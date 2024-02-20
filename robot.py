import numpy as np
from time import time, sleep

from llm import LLM, setup_LMP, cfg_tabletop
from core import AbstractRobot
from controller import Controller
from typing import Tuple, List, Dict
from config.config import RobotConfig, LLMConfig


class Robot(AbstractRobot):
  def __init__(self, env:Tuple[List], cfg=RobotConfig()) -> None:
    self.cfg = cfg
    self.gripper = 1. # 1 means the gripper is open
    self.gripper_timer = 0
    env_info = (env.robots_info, env.objects_info)
    print(f"env_info: {env_info}")
    robots_info, objects_info = env_info
    mpc = Controller(env_info)
    self.lmp = setup_LMP(env, cfg_tabletop, mpc)
    

  def init_states(self, observation:Dict[str, np.ndarray], t:float):
      """ Update simulation time and current state of MPC controller"""
      self.lmp.update_obs(observation)
      # self.MPC.init_states(observation, t, self.gripper==-1.)
      # self.lmp.init(observation, t, self.gripper==-1.)

  def reset(self):
    self.gripper = 1.

  def plan_task(self, user_message:str, base64_image=None) -> str:
    """ Runs the Task Planner by passing the user message and the current frame """
    return self.TP.run(user_message, base64_image, short_history=True)

  def step(self):
    action = [np.array([0., 0., 0., 0., 0., 0., self.gripper])]
    # action = []
    # control: List[np.ndarray] = self.MPC.step()
    # for u in control:
    #   action.append(np.hstack((u, self.gripper)))  
    
    # Logic for opening and closing gripper
    if self.gripper==0 and self.gripper_timer>self.cfg.open_gripper_time: 
      self.gripper = 1.
    else:
      self.gripper_timer += 1

    return action

  def retrieve_trajectory(self):
    # return self.MPC.retrieve_trajectory()
    return []
