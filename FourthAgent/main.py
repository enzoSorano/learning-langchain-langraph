from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END
from enum import Enum
import random


class Hint(str, Enum):
    HIGHER = "higher"
    LOWER = "lower"

class Route(str, Enum):
    LOOP = "loop"
    EXIT = "exit"
    
class Node(str, Enum):
    SETUP = "setup"
    GUESS = "guess"
    FINAL = "final"

#all of the AgentState keys
class sKey(str, Enum):
    ATTEMPTS     = "attempts"
    LOWER_BOUND  = "lower_bound"
    UPPER_BOUND  = "upper_bound"
    PLAYER_NAME  = "player_name"
    HINT         = "hint"
    ACTUAL_NUMBER = "actualNumber"
    GUESS        = "guess"
    GUESSES      = "guesses"


class AgentState(TypedDict):
    attempts: int       # keep track of number of guesses
    lower_bound: int    # current lower bound for the range the number is in
    upper_bound: int    # current upper bound for the range the number is in
    player_name: str    #for the final string
    hint: str           # contains higher or lower
    actualNumber: int   #the number we are trying to guess
    guess: int          #the actual number we are trying to guess
    guesses: List[int] #list of all the guesses for the final output
    


def setup_node(state: AgentState) -> AgentState:
    """Node for greating the user"""
    #zero out counter and guesses
    state[sKey.ATTEMPTS] = 0

    #set upper and lower bounds
    state[sKey.LOWER_BOUND] = 1
    state[sKey.UPPER_BOUND] = 20

    #keep lower bound zero to start
    state[sKey.GUESS] = 0
    state[sKey.HINT] = Hint.HIGHER

    return state

def guess_node(state: AgentState) -> AgentState:
    """"adjust the bounds for the guess and guess the number"""
    #check the hint from the previous round and narrow the bounds
    if state[sKey.HINT] == Hint.HIGHER:
        state[sKey.LOWER_BOUND] = state[sKey.GUESS] + 1  # exclude the previous guess
    elif state[sKey.HINT] == Hint.LOWER:
        state[sKey.UPPER_BOUND] = state[sKey.GUESS] - 1  # exclude the previous guess

    #make a guess within the updated bounds
    state[sKey.GUESS] = random.randint(state[sKey.LOWER_BOUND], state[sKey.UPPER_BOUND])

    #increment the counter and record the guess
    state[sKey.ATTEMPTS] += 1
    state[sKey.GUESSES].append(state[sKey.GUESS])

    #update the hint based on this guess
    if state[sKey.ACTUAL_NUMBER] > state[sKey.GUESS]:
        state[sKey.HINT] = Hint.HIGHER
    elif state[sKey.ACTUAL_NUMBER] < state[sKey.GUESS]:
        state[sKey.HINT] = Hint.LOWER

    return state

def should_continue(state: AgentState) -> str:
    """Read-only router — never modify state here"""
    if state[sKey.ACTUAL_NUMBER] == state[sKey.GUESS]:
        return Route.EXIT
    elif state[sKey.ATTEMPTS] >= 7:
        return Route.EXIT
    else:
        return Route.LOOP

def final_node(state: AgentState) -> AgentState:
    """print the final output"""
    if state[sKey.GUESS] == state[sKey.ACTUAL_NUMBER]:
        print(f"Got it {state[sKey.PLAYER_NAME]}! The number was {state[sKey.ACTUAL_NUMBER]}. It took {state[sKey.ATTEMPTS]} attempts. Guesses: {state[sKey.GUESSES]}")
    else:
        print(f"Sorry {state[sKey.PLAYER_NAME]}, couldn't guess it in 7 attempts! The number was {state[sKey.ACTUAL_NUMBER]}. Guesses: {state[sKey.GUESSES]}")
    return state


if __name__ == "__main__":
    #create graph
    graph = StateGraph(AgentState)

    graph.add_node(Node.SETUP, setup_node)
    graph.add_node(Node.GUESS, guess_node)
    graph.add_node(Node.FINAL, final_node)

    graph.set_entry_point(Node.SETUP)
    graph.add_edge(Node.SETUP, Node.GUESS)
    graph.add_conditional_edges(
        Node.GUESS,
        should_continue,
        {
            Route.LOOP: Node.GUESS,
            Route.EXIT: Node.FINAL
        }
    )
    graph.add_edge(Node.FINAL, END)
    
    app = graph.compile()
    
    answer = app.invoke({
        sKey.ATTEMPTS: 0,
        sKey.LOWER_BOUND: 1,
        sKey.UPPER_BOUND: 20,
        sKey.PLAYER_NAME: "enzo",
        sKey.HINT: Hint.HIGHER,
        sKey.ACTUAL_NUMBER: 14,
        sKey.GUESS: 0,
        sKey.GUESSES: []
    })
    print(answer)


  
