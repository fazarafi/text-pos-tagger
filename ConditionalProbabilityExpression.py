
class ConditionalProbabilityExpression:
    first = 0
    second = 0
    third = 0;

    #Define probability as P(first|second)
    def set_two_param(self, one, two):
        self.first = str(one);
        self.second = str(two);

    #Define probability as P(first\second,third)
    def set_three_param(self, one, two, three):
        self.first = str(one)
        self.second = str(two)
        self.third = str(three);

    def get_first(self):
    	return self.first

    def get_second(self):
    	return self.second

    def get_third(self):
        return self.third

    def is_equal(self, key, num_param):
        if (param == 2):
            one, two = key.split('|')
            if (one == self.first and two == self.second):
                return true
        elif (param == 4):
            one , temp = key.split('|')
            two, third = temp.split(',')
            if (one == self.first and two == self.second and three == self.third):
                return true
        else:
            return false

    def get_key(self):
        if (self.third != 0):
            return self.first + '|' + self.second + ',' + self.third
        else:
            return self.first + '|' + self.second
