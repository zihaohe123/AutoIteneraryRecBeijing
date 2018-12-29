from utils.files_io import *
from utils.baidumap import *
location_interest_graph = open_location_interest_graph()
transfer_info_dict = location_interest_graph.transfer_info_dict
location_coords = location_interest_graph.location_coords
import copy as cp
import json

class Itinerary:
    def __init__(self, trip, start_point_description, end_point_description,
                 start_point, end_point, transfer_info_to_start_point, transfer_info_to_end_point,
                 a1, a2, a3, a4):
        self.start_point_description = start_point_description
        self.end_point_description = end_point_description
        self.start_point = start_point
        self.end_point = end_point
        self.transfer_info_to_start_point = transfer_info_to_start_point
        self.transfer_info_to_end_point = transfer_info_to_end_point
        self.location_coords = trip.location_coords
        self.stay_durations = trip.stay_durations
        self.transfer_durations = trip.transfer_durations
        self.transfer_modes = trip.transfer_modes
        self.interests = trip.interests
        self.score = trip.score_ / (a1**2+a2**2+a3**2+a4**2)**0.5 * 100
        self.transfer_points = trip.transfer_points
        self.location_names = []
        self.results = {}

    def display(self):
        self.location_coords.insert(0, self.start_point)
        self.location_coords.append(self.end_point)

        self.transfer_durations.insert(0, self.transfer_info_to_start_point[0])
        self.transfer_durations.append(self.transfer_info_to_end_point[0])

        self.transfer_points.insert(0, self.transfer_info_to_start_point[1])
        self.transfer_points.append(self.transfer_info_to_end_point[1])

        self.transfer_modes.insert(0, self.transfer_info_to_start_point[2])
        self.transfer_modes.append(self.transfer_info_to_end_point[2])

        self.location_names = [self.start_point_description]
        self.location_names.extend([open_location(loc_coord[0], loc_coord[1]).name for loc_coord in self.location_coords[1:-1]])
        self.location_names.append(self.end_point_description)

        self.results['names'] = self.location_names
        self.results['locations'] = [wgs84_to_bd09(location_coord[0], location_coord[1]) for location_coord in self.location_coords]
        self.results['transfer_points'] = cp.deepcopy(self.transfer_points)
        with open('itinerary.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(self.results, ensure_ascii=False))

            loc_names = self.results['names']
            loc_coords = self.results['locations']
            paths = self.results['transfer_points']
            center_point = "%s,%s" % (loc_coords[0][0], loc_coords[0][1])
            data_info = ''
            for i in range(len(loc_coords)):
                data_info += '[' + str(loc_coords[i][0]) + ',' + str(loc_coords[i][1]) + ',"' + loc_names[i] + '"],\n'
            data_info = data_info[0:-2]

            # print(len(paths))
            points = ''
            for path in paths:
                code = \
                    """
                                	  var sy = new BMap.Symbol(BMap_Symbol_SHAPE_BACKWARD_OPEN_ARROW, {
    scale: 0.6,//图标缩放大小
    strokeColor:'#fff',//设置矢量图标的线填充颜色
    strokeWeight: '2',//设置线宽
});

	var icons = new BMap.IconSequence(sy, '10', '30');
    
    var polyline = new BMap.Polyline([\n 
                    """

                for point in path:
                    code += "new BMap.Point(%s,%s),\n" % (point[0], point[1])
                code += """], {icons: [icons],strokeColor:"green", strokeWeight:5, strokeOpacity:0.8});\nmap.addOverlay(polyline)"""
                points += code + '\n\n'
            # print(points)

            html_code = \
                """
                <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
            <style type="text/css">
            body, html,#allmap {width: 100%%;height: 100%%;overflow: hidden;margin:0;font-family:"微软雅黑";}
            </style>
            <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=RgQ9N7mjmwVFVg9lwoYB7Gfv8csNtifG"></script>
            <title>路线展示</title>
        </head>
        <body>
            <div id="allmap"></div>
        </body>
        </html>
        <script type="text/javascript">
            // 百度地图API功能
            var map = new BMap.Map("allmap");    // 创建Map实例
          map.centerAndZoom(new BMap.Point(%s), 15);

            //添加地图类型控件
            map.addControl(new BMap.MapTypeControl({
                mapTypes:[
                    BMAP_NORMAL_MAP,
                    BMAP_HYBRID_MAP
                ]}));	  
            map.setCurrentCity("北京");          // 设置地图显示的城市 此项是必须设置的
            map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
            
            
    var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
	var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件
	var top_right_navigation = new BMap.NavigationControl({anchor: BMAP_ANCHOR_TOP_RIGHT, type: BMAP_NAVIGATION_CONTROL_SMALL}); //右上角，仅包含平移和缩放按钮
	/*缩放控件type有四种类型:
	BMAP_NAVIGATION_CONTROL_SMALL：仅包含平移和缩放按钮；BMAP_NAVIGATION_CONTROL_PAN:仅包含平移按钮；BMAP_NAVIGATION_CONTROL_ZOOM：仅包含缩放按钮*/
	
	//添加控件和比例尺
    map.addControl(top_left_control);        
    map.addControl(top_left_navigation);     
    map.addControl(top_right_navigation);    
	
            

            var data_info = [
        %s
                            ];
            var opts = {
                        width : 250,     // 信息窗口宽度
                        height: 80,     // 信息窗口高度
                        title : "信息窗口" , // 信息窗口标题
                        enableMessage:true//设置允许信息窗发送短息
                       };
            for(var i=0;i<data_info.length;i++){
                var marker = new BMap.Marker(new BMap.Point(data_info[i][0],data_info[i][1]));  // 创建标注
                if (i==0){
                    var label = new BMap.Label("起点",{offset:new BMap.Size(-30,-10)});
                    marker.setLabel(label);
                }
                if (i==data_info.length-1){
                    var label = new BMap.Label("终点",{offset:new BMap.Size(20,-10)});
                    marker.setLabel(label);
                }
                var content = data_info[i][2];
                map.addOverlay(marker);               // 将标注添加到地图中
                addClickHandler(content,marker);
            }
            function addClickHandler(content,marker){
                marker.addEventListener("click",function(e){
                    openInfo(content,e)}
                );
            }
            function openInfo(content,e){
                var p = e.target;
                var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
                var infoWindow = new BMap.InfoWindow(content,opts);  // 创建信息窗口对象 
                map.openInfoWindow(infoWindow,point); //开启信息窗口
            }


        %s

        </script>
                """ % (center_point, data_info, points)

            with open('./itinerary.html', 'w', encoding='utf-8') as f:
                f.write(html_code)




        location_names = '行程：\n'
        for i in range(len(self.location_names)):
            location_names += self.location_names[i] + '\n|\n'
        location_names = location_names[0:-3]

        stay_durations = '停留时间:'
        for i in range(len(self.stay_durations)):
            stay_durations += self.location_names[i+1] + ':' + str(self.stay_durations[i]) + ', '


        interests = '兴趣度:\n'
        for i in range(len(self.interests)):
            interests += self.location_names[i+1] + ':' + str(self.interests[i]) + '\n'
        interests = interests[0:-1]

        transfer_durations_modes = '转移时间:\n'
        for i in range(len(self.transfer_durations)):
            transfer_durations_modes += self.location_names[i] + '->' + self.location_names[i+1] +':' + str(self.transfer_durations[i]) + ','+self.transfer_modes[i] + '\n'
        transfer_durations_modes = transfer_durations_modes[0:-1]


        exhibition = location_names + '\n\n' + stay_durations +'\n\n' +interests + '\n\n' + transfer_durations_modes + '\n\n得分：' + str(self.score)
        return exhibition

