"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies_made = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._cookies_per_second = 1.0
        self._item_name = None
        self._item_cost = 0.0
        self._history_list = [(self._current_time, 
                               self._item_name, 
                               self._item_cost, 
                               self._cookies_made)]  
                                                     
        
    def __str__(self):
        """
        Return human readable state
        """
        string = "Total cookies made = " + str(self._cookies_made)
        string += ". Current cookies = " + str(self._current_cookies)
        string += ". Current time = " + str(self._current_time)
        string += ". CPS = " + str(self._cookies_per_second)
        string += ".\n History list = " + str(self._history_list)
        
        return string
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cookies_per_second
    
    def get_name(self):
        """
        Return object's name
        """
        return self._item_name
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        history_copy = list(self._history_list)
        return history_copy

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies > 0 and self._current_cookies <= cookies:
            exact_time = (cookies - self._current_cookies) / self._cookies_per_second
            rounded_time = math.ceil(exact_time)
            
            return rounded_time
        
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._cookies_made += time*self._cookies_per_second
            self._current_cookies += time*self._cookies_per_second
            self._current_time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._item_name = item_name
            self._item_cost = cost
            self._current_cookies -= cost
            self._cookies_per_second += additional_cps 
            self._history_list.append((self._current_time, 
                                       self._item_name, 
                                       self._item_cost, 
                                       self._cookies_made))
        else:
            pass
            
   
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    build_clone = build_info.clone()
    simu_state = ClickerState()
    time_left = duration
    
    while(simu_state.get_time() <= duration):
        item = strategy(simu_state.get_cookies(), 
                        simu_state.get_cps(),
                        simu_state.get_history(),
                        time_left, 
                        build_clone)
        
        if item == None:
            break
        elif simu_state.time_until(build_clone.get_cost(item)) > time_left:
            break
        else:
            item_cost = build_clone.get_cost(item)
            add_time = simu_state.time_until(item_cost)
            simu_state.wait(add_time)
            simu_state.buy_item(item, item_cost, build_clone.get_cps(item))
            time_left -= add_time
            build_clone.update_item(item)
    simu_state.wait(time_left)    
    return simu_state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    build_clone = build_info.clone()
    item_list = build_clone.build_items()
    strategy_item = None
    
    for item in item_list:
        
        if time_left * cps + cookies >= build_clone.get_cost(item):
            if strategy_item == None:
                strategy_item = item
                
            elif build_clone.get_cost(item) <= build_clone.get_cost(strategy_item):
                strategy_item = item
    
    return strategy_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    build_clone = build_info.clone()
    item_list = build_clone.build_items()
    strategy_item = None
    
    for item in item_list:
        
        if time_left * cps + cookies >= build_clone.get_cost(item):
            if strategy_item == None:
                strategy_item = item
                
            elif build_clone.get_cost(item) >= build_clone.get_cost(strategy_item):
                strategy_item = item
    
    return strategy_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    build_clone = build_info.clone()
    item_list = build_clone.build_items()
    strategy_item = None
    for item in item_list:
        if time_left * cps + cookies >= build_clone.get_cost(item):
            if strategy_item == None:
                strategy_item = item
            elif build_clone.get_cps(item)/build_clone.get_cost(item) >= build_clone.get_cps(strategy_item)/build_clone.get_cost(strategy_item):
                strategy_item = item
    return strategy_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    
