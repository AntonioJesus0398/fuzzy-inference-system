from src.inference_methods import aggregate
from src.defuzzification import center_of_area, bisector_of_area, mean_of_maximum
from src.classes import FuzzySet

class FuzzyInferenceSystem:

    def __init__(self, rule_base):
        self.rule_base = rule_base

    def solve(self, _input, inference_method="Mamdani", defuzzification_method="coa"):

        # perform the inference method
        if not inference_method in ["Mamdani", "Larsen"]:
            raise ValueError("Inapropiate fuzzification method. The available values are: Mamdani, Larsen")
        fuzzy_result = aggregate(_input, self.rule_base, method=inference_method)

        # apply the defuzzification operator
        _deffuzification_method = None
        if defuzzification_method == "coa":
            _deffuzification_method = center_of_area
        elif defuzzification_method == "boa":
            _deffuzification_method = bisector_of_area
        elif defuzzification_method == "mom":
            _deffuzification_method = mean_of_maximum
        else:
            raise ValueError("Inapropiate defuzzifiaction method. The available values are: mom, coa, boa")
        deffuzified_result = {variable_name: _deffuzification_method(fuzzy_result[variable_name], step=self.rule_base.control_variables[variable_name].step_size) for variable_name in fuzzy_result.keys()}

        # unscale the result
        unscaled_result = {variable_name: self.rule_base.control_variables[variable_name].unscaling_function(deffuzified_result[variable_name]) for variable_name in deffuzified_result}

        return unscaled_result
