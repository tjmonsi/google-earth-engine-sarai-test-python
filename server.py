import os;
import config;
import ee;
import webapp2;
import datetime;
import json;

class MainApi(webapp2.RequestHandler):
  def get(self):
    startDateStr = self.request.get('date');
    days = self.request.get('range');
    startDate = datetime.datetime.strptime(startDateStr, "%Y-%m-%d");
    endDate = startDate + datetime.timedelta(days=10);
    endDateStr = endDate.strftime("%Y-%m-%d");
    ee.Initialize(config.EE_CREDENTIALS);
    
    geometry = ee.Geometry.Polygon(ee.List([
      [127.94248139921513,5.33459854167601],
      [126.74931782819613,11.825234466620996],
      [124.51107186428203,17.961503806746318],
      [121.42999903167879,19.993626604011016],
      [118.25656974884657,18.2117821750514],
      [116.27168958893185,6.817365082528201],
      [122.50121143769957,3.79887124351577],
      [127.94248139921513,5.33459854167601]
      ]), 
      'EPSG:4326',
      True
    );
    
    imageCollection = ee.ImageCollection("LANDSAT/LC8_L1T_8DAY_NDVI");
    hansenImage = ee.Image('UMD/hansen/global_forest_change_2013');
    data = hansenImage.select('datamask');
    mask = data.eq(1);
    images = imageCollection.filterDate(startDateStr, endDateStr).filterBounds(geometry);
    maskedDifference = images.median().updateMask(mask);
    mapObject = maskedDifference.getMapId({'palette': 'FFFFFF, 004400', 'min': -0.31, 'max': 0.79});
    mapId = mapObject['mapid']
    mapToken = mapObject['token']
    
    self.response.headers['Content-Type'] = 'application/json';   
    obj = {
      'success': True, 
      'mapId': mapId,
      'mapToken': mapToken
    };
    self.response.out.write(json.dumps(obj));
    
app = webapp2.WSGIApplication([('/', MainApi)], debug=True);

def main():
    from paste import httpserver;
    httpserver.serve(app, host='0.0.0.0', port='8080');

if __name__ == '__main__':
    main();