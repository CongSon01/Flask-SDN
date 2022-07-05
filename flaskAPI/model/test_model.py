import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/model')
import LinkCost
import LearnWeightModel

print(LearnWeightModel.get_label('of:0000000000000005', 'of:0000000000000002'))