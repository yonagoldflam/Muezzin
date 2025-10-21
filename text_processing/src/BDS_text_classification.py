class BDSTextClassification:

    @staticmethod
    def calculate_hostile_score(text: str, hostile_decoding_list: list[str], not_hostile_decoding_list: list[str]) -> float:
        score: int = 0
        for hostile in hostile_decoding_list:
            score += text.count(hostile) * 2
        for not_hostile in not_hostile_decoding_list:
            score += text.count(not_hostile)
        if score:
            return len(text) / score
        return 0
    @staticmethod
    def threat_level_field(score: int) -> dict[str, str]:
        high_threat_field: dict[str, str] = {'bds_threat_level': 'high'}
        medium_threat_field: dict[str, str] = {'bds_threat_level': 'medium'}
        none_threat_field: dict[str, str] = {'bds_threat_level': 'none'}
        if score < 40:
            return high_threat_field
        elif score < 100:
            return medium_threat_field
        else:
            return none_threat_field
    @staticmethod
    def is_bds(score: int) -> dict[str, bool]:
        is_bds_field: dict[str, bool] = {'is_bds': True}
        not_bds_field: dict[str, bool] = {'is_bds': False}
        if score:
            if score < 100:
                return is_bds_field
            else:
                return not_bds_field
        return not_bds_field



