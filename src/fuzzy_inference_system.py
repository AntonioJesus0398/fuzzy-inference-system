from src.inference_methods import aggregate
from src.defuzzification import center_of_area, bisector_of_area, mean_of_maximum
from src.classes import FuzzySet


# from inference_methods import aggregate
# from defuzzification import center_of_area, bisector_of_area, mean_of_maximum
# from classes import FuzzySet

class FuzzyInferenceSystem:

    def __init__(self, rule_base, inference_method="Mamdani", defuzzification_method="coa"):
        self.rule_base = rule_base
        self.inference_method = inference_method

        if defuzzification_method == "coa":
            self.defuzzification_method = center_of_area
        elif defuzzification_method == "boa":
            self.defuzzification_method = bisector_of_area
        elif defuzzification_method == "mom":
            self.defuzzification_method = mean_of_maximum
        else:
            raise ValueError(f"'{defuzzification_method}' is not a valid defuzzification method")

    def solve(self, _input):

        # perform the inference method
        fuzzy_result = aggregate(_input, self.rule_base, method=self.inference_method)

        # apply the defuzzification operator
        deffuzified_result = {variable_name: self.defuzzification_method(fuzzy_result[variable_name], step=self.rule_base.control_variables[variable_name].step_size) for variable_name in fuzzy_result.keys()}

        # unscale the result
        unscaled_result = {variable_name: self.rule_base.control_variables[variable_name].unscaling_function(deffuzified_result[variable_name]) for variable_name in deffuzified_result}

        return unscaled_result
