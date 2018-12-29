import json

with open('./itinerary.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

    loc_names = results['names']
    loc_coords = results['locations']
    paths =  results['transfer_points']
    center_point = "%s,%s" % (loc_coords[0][0], loc_coords[0][1])
    data_info = ''
    for i in range(len(loc_coords)):
        data_info += '[' + str(loc_coords[i][0]) + ',' + str(loc_coords[i][1]) + ',"'+loc_names[i]+'"],\n'
    data_info = data_info[0:-2]

    # print(len(paths))
    points = ''
    for path in paths:
        code = \
        "var polyline = new BMap.Polyline([\n "
        for point in path:
            code += "new BMap.Point(%s,%s),\n" % (point[0], point[1])
        code += """], {strokeColor:"green", strokeWeight:5, strokeOpacity:0.8});\nmap.addOverlay(polyline)"""
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

    with open('./itinerary.html', 'w',encoding='utf-8') as f:
        f.write(html_code)

