class BDSTextClassification:

    @staticmethod
    def calculate_hostile_score(text, hostile_decoding_list, not_hostile_decoding_list):
        score = 0
        for hostile in hostile_decoding_list:
            score += text.count(hostile) * 2
        for not_hostile in not_hostile_decoding_list:
            score += text.count(not_hostile)
        if score:
            return len(text) / score
        return 0
    @staticmethod
    def threat_level_field(score):
        high_threat_field = {'bds_threat_level': 'high'}
        medium_threat_field = {'bds_threat_level': 'medium'}
        none_threat_field = {'bds_threat_level': 'none'}
        if score < 40:
            return high_threat_field
        elif score < 100:
            return medium_threat_field
        else:
            return none_threat_field
    @staticmethod
    def is_bds(score):
        is_bds_field = {'is_bds': 'True'}
        not_bds_field = {'is_bds': 'False'}
        if score:
            if score < 100:
                return is_bds_field
            else:
                return not_bds_field
        return not_bds_field



