import os;
import config;
import ee;
import webapp2;
import datetime;
import json;

class MainApi(webapp2.RequestHandler):
  def get(self):
    startDateStr = self.request.get('date');
    startDate = datetime.datetime.strptime(startDateStr, "%Y-%m-%d");
    endDate = startDate + datetime.timedelta(days=10);
    endDateStr = endDate.strftime("%Y-%m-%d");
    self.response.headers['Content-Type'] = 'application/json';   
    obj = {
      'success': True, 
      'start-date': startDateStr,
      'end-date': endDateStr
    };
    self.response.out.write(json.dumps(obj));
    
app = webapp2.WSGIApplication([('/', MainApi)], debug=True);

def main():
    from paste import httpserver;
    httpserver.serve(app, host='0.0.0.0', port='8080');

if __name__ == '__main__':
    main();