from flask import Flask
from flask_restplus import Resource, Api
from PlanningEngine import PlanningEngine
import Common.config as config

app = Flask(__name__)
api = Api(app)
# LOG = logging.getLogger(__name__)
planningEngine = PlanningEngine()

Individual_Model = api.model('input', {})


@api.route('/ValidateHousehold')
class Process(Resource):
    @api.expect(Individual_Model)
    def post(self):
        config.load_logging_config()
        request = api.payload
        return planningEngine.validateHouseHold(request)


@api.route('/Simulation/Run')
class ssind(Resource):
    @api.expect(Individual_Model)
    def post(self):
        request = api.payload
        return planningEngine.runSimulation(request)


if __name__ == '__main__':
    app.run('127.0.0.1', 50000, debug=True)
