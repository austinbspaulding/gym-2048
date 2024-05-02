#!/usr/bin/env python3

import gymnasium as gym
import gym_2048
import random
from copy import deepcopy
from typing import Callable, Dict

m = gym_2048.Gym2048Model

def manhattan(i1, i2):
    x1 = i1 % 4
    x2 = i2 % 4
    y1 = (i1 - x1) / 4
    y2 = (i2 - x2) / 4

    return abs(x1 - x2) + abs(y1 - y2)

class Agent:
    action: Callable[[gym_2048.Gym2048State], int]
    name: str
    description: str

    def __init__(self, name, description):
        self.name = name
        self.description = description

random_agent = Agent("random_agent", "makes a fully random decision")

def f(state: gym_2048.Gym2048State):
    action = random.choice(m.ACTIONS(state))
    return action
random_agent.action = f

simple_reflex_agent = Agent("simple_reflex_agent_manhattan", "picks the move that results in the best score according to cells values and their manhattan distance from the top left corner.")
def f(state: gym_2048.Gym2048State): # type: ignore[no-redef]

    def score(state: gym_2048.Gym2048State):
        curr_score = 0
        for i, v in enumerate(state._state):
            dist = manhattan(0, i) + 1
            curr_score += v / dist
        return curr_score

    bestScore = 0
    for a in m.ACTIONS(state):
        s = deepcopy(state)
        s.simulate_move(a)

        if 2048 in s._state:
            return a

        curr_score = score(s)

        if curr_score > bestScore:
            bestScore = curr_score
            bestAction = a

    return bestAction 
simple_reflex_agent.action = f

simple_reflex_agentv2 = Agent("simple_reflex_agent_manhattan+count", "picks the move that results in the best score according to cells values and their manhattan distance from the top left corner, as well as the number of each cell.")
def f(state: gym_2048.Gym2048State): # type: ignore[no-redef]

    def score(state: gym_2048.Gym2048State):
        curr_score = 0
        counts: Dict[int, int] = {}
        for v in state._state:
            if counts.get(v) == None:
                counts[v] = 1
            else:
                counts[v] = counts[v] + 1

        for i, v in enumerate(state._state):
            dist = manhattan(0, i) + 1
            curr_score += v / dist / counts[v]
        return curr_score

    bestScore = 0
    for a in m.ACTIONS(state):
        s = deepcopy(state)
        s.simulate_move(a)

        if 2048 in s._state:
            return a

        curr_score = score(s)

        if curr_score > bestScore:
            bestScore = curr_score
            bestAction = a

    return bestAction 
simple_reflex_agentv2.action = f

simple_reflex_agentv3 = Agent("simple_reflex_agent_peekahead", "picks the move that results in the best score according to cells values and their manhattan distance from the top left corner, while looking a few steps ahead")
def f(state: gym_2048.Gym2048State): # type: ignore[no-redef]
    def score(s: gym_2048.Gym2048State):
        curr_score = 0
        for i, v in enumerate(state._state):
            dist = manhattan(0, i) + 1
            curr_score += v / dist
        return curr_score
    
    def scorePeekAhead(state: gym_2048.Gym2048State, steps):
        if steps == 0:
            return score(state)
        if m.GOAL_TEST(state):
                return score(state)
        
        bestScore = 0
        curr_score: int = 0
        for a in m.ACTIONS(state):
            s = deepcopy(state)
            s.simulate_move(a)

            if 2048 in s._state:
                return score(state)
            
            curr_score = score(s)
            if curr_score > bestScore:
                bestScore = curr_score

            curr_score = scorePeekAhead(s, steps - 1)
            if curr_score > bestScore:
                bestScore = curr_score

        return bestScore
    
    bestScore = 0
    for a in m.ACTIONS(state):
        s = deepcopy(state)
        s.simulate_move(a)
        curr_score = scorePeekAhead(state, 1)
        if(curr_score) > bestScore:
            bestScore = curr_score
            bestAction = a

    return bestAction
simple_reflex_agentv3.action = f

simple_reflex_agentv4 = Agent("simple_reflex_agent_distance_aware", "picks the move that results in the best score according to cells values relative to other cells of the same type")
def f(state: gym_2048.Gym2048State): # type: ignore[no-redef]

    def score(state: gym_2048.Gym2048State):
        curr_score = 0
        closests: Dict[int, int] = {}
        for i, v in enumerate(state._state):
            if closests.get(v) == None:
                closests[v] = i
            else:
                closest = closests[v]
                if manhattan(0, i) < manhattan(0, closest):
                    closest = i
                closests[v] = closest
            
            for k, closest in closests.items():
                for i, v in enumerate(state._state):
                    if v == k:
                        curr_score += v / (manhattan(closest, i) + 1)
        
        return curr_score
                


    bestScore = 0
    for a in m.ACTIONS(state):
        s = deepcopy(state)
        s.simulate_move(a)

        if 2048 in s._state:
            return a

        curr_score = score(s)

        if curr_score > bestScore:
            bestScore = curr_score
            bestAction = a

    return bestAction 
simple_reflex_agentv4.action = f

simple_reflex_agentv5 = Agent("simple_reflex_agent_distance_aware+manhattan", "picks the move that results in the best score according to cells values relative to other cells of the same type")
def f(state: gym_2048.Gym2048State): # type: ignore[no-redef]

    def score(state: gym_2048.Gym2048State):
        curr_score = 0
        closests: Dict[int, int] = {}
        for i, v in enumerate(state._state):
            if closests.get(v) == None:
                closests[v] = i
            else:
                closest = closests[v]
                if manhattan(0, i) < manhattan(0, closest):
                    closest = i
                closests[v] = closest
            
            for k, closest in closests.items():
                for i, v in enumerate(state._state):
                    if v == k:
                        curr_score += v / (manhattan(closest, i) + manhattan(0, i) + 1) 
        
        return curr_score

    bestScore = 0
    for a in m.ACTIONS(state):
        s = deepcopy(state)
        s.simulate_move(a)

        if 2048 in s._state:
            return a

        curr_score = score(s)

        if curr_score > bestScore:
            bestScore = curr_score
            bestAction = a

    return bestAction 
simple_reflex_agentv5.action = f

simple_reflex_agentv6 = Agent("simple_reflex_agent_distance_aware+manhattan+peekahead", "picks the move that results in the best score according to cells values relative to other cells of the same type, peeking ahead a few moves")
def f(state: gym_2048.Gym2048State): # type: ignore[no-redef]

    def score(state: gym_2048.Gym2048State):
        curr_score = 0
        closests: Dict[int, int] = {}
        for i, v in enumerate(state._state):
            if closests.get(v) == None:
                closests[v] = i
            else:
                closest = closests[v]
                if manhattan(0, i) < manhattan(0, closest):
                    closest = i
                closests[v] = closest
            
            for k, closest in closests.items():
                for i, v in enumerate(state._state):
                    if v == k:
                        curr_score += v / (manhattan(closest, i) + manhattan(0, i) + 1) 
        
        return curr_score
    
    def scorePeekAhead(state: gym_2048.Gym2048State, steps):
        if steps == 0:
            return score(state)
        if m.GOAL_TEST(state):
                return score(state)
        
        bestScore = 0
        curr_score: int = 0
        for a in m.ACTIONS(state):
            s = deepcopy(state)
            s.simulate_move(a)

            if 2048 in s._state:
                return score(state)
            
            curr_score = score(s)
            if curr_score > bestScore:
                bestScore = curr_score

            curr_score = scorePeekAhead(s, steps - 1)
            if curr_score > bestScore:
                bestScore = curr_score

        return bestScore
    
    bestScore = 0
    for a in m.ACTIONS(state):
        s = deepcopy(state)
        s.simulate_move(a)
        curr_score = scorePeekAhead(state, 2)
        if(curr_score) > bestScore:
            bestScore = curr_score
            bestAction = a

    return bestAction
simple_reflex_agentv6.action = f

def main():
    render_mode = None
    # render_mode = "ansi"
    # render_mode = "human"

    env = gym.make('gym_2048/Gym2048-v0', render_mode=render_mode)

    agents = [
        # random_agent,
        simple_reflex_agent,
        # simple_reflex_agentv2,
        # simple_reflex_agentv3,
        simple_reflex_agentv4,
        simple_reflex_agentv5,
        # simple_reflex_agentv6,
    ]

    # class AgentResult():
    #     agent: Agent
    #     scores: List[int] = []
    #     bestScore = 0
    #     bestState: gym_2048.Gym2048State

    #     def __init__(self, agent):
    #         self.agent = agent

    out = []
    attempts = 1000
    for agent in agents:
        totalScore = 0
        bestScore = 0
        for i in range(attempts):
            observation, info = env.reset()
            state = gym_2048.Gym2048State()
            state.observation = observation
            
            terminated = truncated = False
            score = 0

            if render_mode == "ansi":
                print("Current state:")
                print(env.render())

            DS = gym_2048.Gym2048DIRECTIONS
            while not (terminated or truncated):
                action = agent.action(state)
                
                if render_mode == "ansi":
                    action_name = ""
                    match action:
                        case DS.UP:
                            action_name = "up"
                        case DS.DOWN:
                            action_name = "down"
                        case DS.LEFT:
                            action_name = "left"
                        case DS.RIGHT:
                            action_name = "right"
                    print()
                    print(f"Action: moving {action_name}.")

                observation, reward, terminated, truncated, info = env.step(action)
                state.observation = observation
                if render_mode == "ansi":
                    print("Current state:")
                    print(env.render())
            score = m.HEURISTIC(state)
            totalScore += score
            if score > bestScore:
                bestScore = score
                bestState = state
            if True:
                print(f"Attempt {i + 1} of agent {agent.name} produced score {score}")
                print(f"this agent has a current average score of {totalScore / (i + 1)}")
                print(f"this agent has a current best score of {bestScore}")
                print("this attempts final board layout was")
                print(state)
        out.append((totalScore / attempts, bestScore, bestState, agent.name))

    print()
    print("==========================================")
    print()
    out.sort(reverse=True)
    for score, best, bestState, name in out:
        print(f"{name}'s best state had a score of {m.HEURISTIC(bestState)}")
        print(bestState)
    for score, best, bestState, name in out:
        print(f"{name} had an average score of {score} and a best score of {best} across {attempts} attempts.")
    env.close()
    return

if __name__ == "__main__":
    main()
    

