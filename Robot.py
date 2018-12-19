import random

class Robot(object):

    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon0=0.5):

        self.maze = maze
        self.valid_actions = self.maze.valid_actions
        self.state = None
        self.action = None

        # Set Parameters of the Learning Robot
        self.alpha = alpha
        self.gamma = gamma

        self.epsilon0 = epsilon0
        self.epsilon = epsilon0
        self.t = 0

        self.Qtable = {}
        self.reset()

    def reset(self):
        """
        Reset the robot
        """
        self.state = self.sense_state()
        self.create_Qtable_line(self.state)

    def set_status(self, learning=False, testing=False):
        """
        Determine whether the robot is learning its q table, or
        exceuting the testing procedure.
        """
        self.learning = learning
        self.testing = testing

    def update_parameter(self):
        """
        Some of the paramters of the q learning robot can be altered,
        update these parameters when necessary.
        """
        if self.testing:
            # TODO 1. No random choice when testing
            pass
        else:
            # TODO 2. Update parameters when learning
            self.t += 1
            if(self.epsilon < 0.01):
            	self.epsilon = 0.01
            else:
            	self.epsilon = round(self.epsilon - 0.01*self.t,2)
            #print("&&&&&&&&&& update_parameter &&&&&&&&&&&&&&&&&&&&&&&&&&&&&",self.epsilon,self.t)
        return self.epsilon

    def sense_state(self):
        """
        Get the current state of the robot. In this
        """

        # TODO 3. Return robot's current state
        #返回robot当前位置
        return self.maze.sense_robot()

    def create_Qtable_line(self, state):
        """
        Create the qtable with the current state
        """
        # TODO 4. Create qtable with current state
        # Our qtable should be a two level dict,
        # Qtable[state] ={'u':xx, 'd':xx, ...}
        # If Qtable[state] already exits, then do
        # not change it.
        #print("create_Qtable_line",state,self.Qtable)
        #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        if(state not in self.Qtable):
        	self.Qtable[state] = {'u':0.0,'r':0.0,'d':0.0,'l':0.0}



    def choose_action(self):
        """
        Return an action according to given rules
        """
        def is_random_exploration():

            # TODO 5. Return whether do random choice
            # hint: generate a random number, and compare
            # it with epsilon
            return random.random() < self.epsilon
	        	


        if self.learning:
            if is_random_exploration():
                # TODO 6. Return random choose aciton
                m_actions_num = len(self.maze.valid_actions)
                #print("choose_action:random_choose")
                return self.maze.valid_actions[random.randint(0,m_actions_num-1)]
            else:
                # TODO 7. Return action with highest q value
                state_q = self.Qtable[self.state]
                choose_action = max(state_q,key=state_q.get)
                #print("choose_action highest",choose_action)
                return choose_action
        elif self.testing:
            # TODO 7. choose action with highest q value
            state_q = self.Qtable[self.state]
            choose_action = max(state_q,key=state_q.get)
            #print("choose_action highest",choose_action)
            return choose_action
        else:
            # TODO 6. Return random choose aciton
            m_actions_num = len(self.maze.valid_actions)
            #print("choose_action:not test:random_choose")
            return self.maze.valid_actions[random.randint(0,m_actions_num-1)]

    def update_Qtable(self, r, action, next_state):
        """
        Update the qtable according to the given rule.
        """
        if self.learning:
            # TODO 8. When learning, update the q table according
            # to the given rules
            #print("update_Qtable:next_state",next_state)
            #print("update_Qtable:action",action)
            #print(type(self.gamma))
            #print(type(max(self.Qtable[next_state].values())))
            q_temp = r+self.gamma*max(self.Qtable[next_state].values())
            self.Qtable[self.state][action] = round((1-self.alpha)*self.Qtable[self.state][action] + self.alpha*(r+self.gamma*q_temp),2)
            #print("update_Qtable***********",self.Qtable[self.state])

    def update(self):
        """
        Describle the procedure what to do when update the robot.
        Called every time in every epoch in training or testing.
        Return current action and reward.
        """
        self.state = self.sense_state() # Get the current state
        #print("state:",self.state)
        
        self.create_Qtable_line(self.state) # For the state, create q table line

        action = self.choose_action() # choose action for this state
        
        reward = self.maze.move_robot(action) # move robot for given action
        #print("****************action *****************************",action)
        #print("----------------reward -----------------------------",reward)
        next_state = self.sense_state() # get next state
        #print("next_state:",next_state)
        self.create_Qtable_line(next_state) # create q table line for next state
        #print("next_state_q",self.Qtable)
        if self.learning and not self.testing:
            self.update_Qtable(reward, action, next_state) # update q table
            self.update_parameter() # update parameters
		
        return action, reward
