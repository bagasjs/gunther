from gunther.analyzers.slither_analyzer import SlitherAnalyzer
from gunther.analyzers.core import Analyzer, FindingSeverity, AnalysisResult

list_of_analyzers = {
    "slither": SlitherAnalyzer(),
}
