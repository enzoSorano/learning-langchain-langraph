from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END
import random


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
    state['attempts'] = 0
    #state['guesses'] = []

    #set upper and lower bounds
    state['lower_bound'] = 1
    state['upper_bound'] = 20

    #keep lower bound zero to start
    state['guess'] = 0
    state['hint'] = "higher"
    
    return state

def guess_node(state: AgentState) -> AgentState:
    """"adjust the bounds for the guess and guess the number"""
    #check the hint from the previous round and narrow the bounds
    if state['hint'] == "higher":
        state['lower_bound'] = state['guess'] + 1  # exclude the previous guess
    elif state['hint'] == "lower":
        state['upper_bound'] = state['guess'] - 1  # exclude the previous guess

    #make a guess within the updated bounds
    state['guess'] = random.randint(state['lower_bound'], state['upper_bound'])

    #increment the counter and record the guess
    state['attempts'] += 1
    state['guesses'].append(state['guess'])

    #update the hint based on this guess
    if state['actualNumber'] > state['guess']:
        state['hint'] = "higher"
    elif state['actualNumber'] < state['guess']:
        state['hint'] = "lower"

    return state

def should_continue(state: AgentState) -> str:
    """Read-only router — never modify state here"""
    if state['actualNumber'] == state['guess']:
        return "exit"
    elif state['attempts'] >= 7:
        return "exit"
    else:
        return "loop"

def final_node(state: AgentState) -> AgentState:
    """print the final output"""
    if state['guess'] == state['actualNumber']:
        print(f"Got it {state['player_name']}! The number was {state['actualNumber']}. It took {state['attempts']} attempts. Guesses: {state['guesses']}")
    else:
        print(f"Sorry {state['player_name']}, couldn't guess it in 7 attempts! The number was {state['actualNumber']}. Guesses: {state['guesses']}")
    return state


if __name__ == "__main__":
    #create graph
    graph = StateGraph(AgentState)

    graph.add_node("setup", setup_node)
    graph.add_node("guess", guess_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("setup")
    graph.add_edge("setup", "guess")
    graph.add_conditional_edges(
        "guess",
        should_continue,
        {
            "loop": "guess",
            "exit": "final"
        }
    )
    graph.add_edge("final", END)
    
    app = graph.compile()
    
    answer = app.invoke({
        "attempts": 0,
        "lower_bound": 1,
        "upper_bound": 20,
        "player_name": "enzo",
        "hint": "higher",
        "actualNumber": 14,
        "guess": 0,
        "guesses": []
    })
    print(answer)


  
