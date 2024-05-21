import os
import cv2
import gym
import json
import panda_gym
import numpy as np
from PIL import Image
from tqdm import tqdm
from typing import List
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from robot import Robot
from db import Base, Episode, Epoch
from core import AbstractSimulation, BASE_DIR
from config.config import SimulationConfig, RobotConfig

import base64

def image_to_base64(image_path) -> str:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


def make_plan(robot:Robot, user_message:str="", user_image=None) -> str:
    plan:dict = robot.plan_task(user_message, user_image)
    print("plan:", plan)
    pretty_msg = "Tasks:\n"
    pretty_msg += "".join([f"{i+1}. {task}\n" for i, task in enumerate(plan["tasks"])])
    return pretty_msg

'''
def reset(self):
    # reset pand env
    self.observation = self.env.reset() # how does this work? there is no explicit implementation of reset but only abstract.
    # reset robot
    self.robot.reset() #llm not working
    # reset controller
    self.robot.init_states(self.observation, self.t) #mpc not working
    # reset task counter
    self.plan = None
    self.optimizations = [] 
    self.task_counter = 0
    # init list of RGB frames if wanna save video
    if self.save_video:
        self._save_video()
    if self.cfg.logging:
        if self.session is not None:
            self.episode.state_trajectories = json.dumps(self.state_trajectories)
            self.episode.mpc_solve_times = json.dumps(self.mpc_solve_times)
            if self.cfg.logging_video:
                self._save_video()
            self.session.commit()
            self.state_trajectories = []
            self.mpc_solve_times = []
            self.session.close()
        self.session = self.Session()
        self.episode = Episode()  # Assuming Episode has other fields you might set
        self.session.add(self.episode)
        self.session.commit()
        n_episodes = len(os.listdir(f"data/{self.cfg.method}/images"))
        self.episode_folder = f"data/{self.cfg.method}/images/{n_episodes}"
        os.mkdir(self.episode_folder)
        self.video_path = os.path.join(BASE_DIR, f"data/{self.cfg.method}/videos/{self.cfg.task}_{n_episodes}_full.mp4")
        self.video_path_logging = os.path.join(BASE_DIR, f"data/{self.cfg.method}/videos/{self.cfg.task}/{self.episode.id}.mp4")
    
    # init list of RGB frames if wanna save video
    if self.save_video:
        self._save_video()
    self.frames_list = []
    self.frames_list_logging = []
    self.t = 0.
    self.epoch = 0
'''

if __name__=="__main__":
    
    env_info = ([{'name': '', 'x0': np.array([ 3.84396701e-02, -2.19447219e-12,  1.97400143e-01]), 'euler0': np.array([3.14159265, 0.        , 0.        ])}], [{'name': 'blue_cube'}, {'name': 'green_cube'}, {'name': 'orange_cube'}, {'name': 'red_cube'}, {'name': 'flower'}])
    cfg = RobotConfig("Cubes")
    r = Robot(env_info, cfg)
    image = "data/DBs/cubes_objective.db"

    for _ in range(3):
        # run test
        make_plan(r, "what objects are present?", image)
