

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
    numberOfTargets = None
    multipleArrowsPerTarget = None
    possibleValues = []
    targetBonus = None
    numberOfRuns = None

    @property
    def possibleStringValues(self):
        return ["{}".format(value) for value in self.possibleValues]


class StyleSettings(object):
    def createRunSettings(self):
        raise NotImplementedError


class HungarianStyleSettings(StyleSettings):
    def createRunSettings(self):
        for __ in range(HungarianRunSettings.numberOfRuns):
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
    possibleValues = [0, 2, 3, 4]
    numberOfRuns = 2  # 9 #for test purposes


class KoreanStyleSettings(StyleSettings):

    koreanRunsSettings = []

    def createRunSettings(self):
        for koreanRunsSettings in self.koreanRunsSettings:
            for __ in range(koreanRunsSettings.numberOfRuns):
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

class FFEStyleSettings(StyleSettings):

    runsSettings = []

    def createRunSettings(self):
        for runSetting in self.runsSettings:
            for __ in range(runSetting.numberOfRuns):
                yield runSetting()

class FFEWalkRunSettings(RunSettings):
    """
    Parameters for walk runs in FFE competitions
    """
    timeBonus = 0
    maxTimeBonus = 0
    timeMalus = 0
    multipleArrowsPerTarget = True
    possibleValues = [2,3,4]

class FFECanterRunSettings(RunSettings):
    """
    Parameters for times run in FFE competitions
    """
    eliminatingTime = self.maxTime +3
    maxTimeBonus = 3

class FFEWalkClub1RunSettings(FFEWalkRunSettings):
    trackLength = 60
    numberOfRuns = 1

class FFEWalkClub2RunSettings(FFEWalkRunSettings):
    trackLength = 40
    numberOfRuns = 2

class FFEClub1HungarianRunSettings(FFECanterRunSettings):
    """
    Parameters for a hungarian run, FFE Club 1 flavour
    """
    trackLength = 60
    maxTime = 12
    timeBonus = 1
    multipleArrowsPerTarget = True
    numberOfTargets = 1
    possibleValues = [2, 3, 4]
    numberOfRuns = 5

class FFEClub1Korean1RunSettings(Korean1RunSettings):
    trackLength = 60
    maxTime = 10
    numberOfRuns = 4

class FFEClub1Korean3RunSettings(Korean3RunSettings):
    trackLength = 60
    maxTime = 10
    numberOfRuns = 2

class FFEClub1HungarianStyleSetting(FFEStyleSettings):
    runsSettings = [FFEWalkClub1RunSettings, FFEClub1HungarianRunSettings]

class FFEClub1KoreanStyleSetting(FFEStyleSettings):
    runsSettings = [FFEClub1Korean1RunSettings, FFEClub1Korean3RunSettings]
