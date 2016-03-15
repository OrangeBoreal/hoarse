

class RunSettings(object):
    """
    Parameters needed by a run for all styles
    """
    trackLength = None
    maxTime = None
    eliminatingTime = None
    timeBonus = None
    maxTimeBonus = None
    timeMalus = None
    numberOfTargets  = None
    multipleArrowsPerTarget = None
    possibleValues = None
    targetBonus = None
    numberOfRuns = None
    numberOfUntimedRuns = None


class StyleSettings(object):
    def createRunSettings(self):
        raise NotImplementedError

class HungarianStyleSettings(StyleSettings):
    def createRunSettings(self):
        for i in range(HungarianRunSettings.numberOfRuns):
            yield HungarianRunSettings()

class HungarianRunSettings(RunSettings):
    """
    Parameters for a hungarian run
    """
    trackLength = 99
    maxTime = 20
    eliminatingTime = 20
    timeBonus = 1
    multipleArrowsPerTarget = True
    numberOfTargets = 1
    possibleValues = [2, 3, 4]
    numberOfRuns = 3 #9 #for test purposes

class KoreanStyleSettings(StyleSettings):

    koreanRunsSettings = None

    def createRunSettings(self):
        for koreanRunsSettings in self.koreanRunsSettings:
            for i in range(koreanRunsSettings.numberOfRuns):
                yield koreanRunsSettings()


class KoreanRunSettings(RunSettings):
    trackLength = 90
    maxTime = 14
    timeBonus = 1
    timeMalus = 1
    multipleArrowsPerTarget = False
    possibleValues = [0, 1, 2, 3, 4, 5]
    numberOfRuns = 2


class Korean1RunSettings(KoreanRunSettings):
    """
    Parameters for a korean single shoot run
    """
    numberOfTargets = 1


class Korean2RunSettings(KoreanRunSettings):
    """
    Parameters for a korean double shoot run
    """
    numberOfTargets = 2
    targetBonus = [2]


class Korean3RunSettings(KoreanRunSettings):
    """
    Parameters for a korean triple shoot run
    """
    numberOfTargets = 3
    trackLength = 120
    maxTime = 18
    targetBonus = [3]


class Korean5RunSettings(KoreanRunSettings):
    """
    Parameters for a korean multi-shoot run
    """
    numberOfTargets = 5
    trackLength = 150
    maxTime = 23
    targetBonus = [3, 5]


class Korean125StyleSettings(KoreanStyleSettings):
    koreanRunsSettings = [Korean1RunSettings, Korean2RunSettings, Korean5RunSettings]


class Korean123StyleSettings(KoreanStyleSettings):
    koreanRunsSettings = [Korean1RunSettings, Korean2RunSettings, Korean3RunSettings]


class Korean235StyleSettings(KoreanStyleSettings):
    koreanRunsSettings = [Korean2RunSettings, Korean3RunSettings, Korean5RunSettings]
    
    
class FFEClub1HungarianRunSettings(RunSettings):
    """
    Parameters for a hungarian run
    """
    trackLength = 60
    maxTime = 12
    eliminatingTime = 12
    timeBonus = 1
    multipleArrowsPerTarget = True
    numberOfTargets = 1
    possibleValues = [2, 3, 4]
    numberOfRuns = 9
