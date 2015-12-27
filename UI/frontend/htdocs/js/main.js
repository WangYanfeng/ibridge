// longtitude
 $(function(){
  longtitude=30.2653;
  latitude=114.2320;
  var chart=new Array();
  var sensor_type="stress";//实时采集中的类型
  var analyse_type="stress";//数据分析的类型
  var analyse_time=7;
  var analyse_data_type="stress";
  var bridge_id=$("#bridge_id").text();
  var sensor_sort_num=$("#stress").attr("value");//实时采集某类传感器个数
  var analyse_sensor_sort_num=$("#stress").attr("value");
  var data_num;//采集数据个数。点击查看详情个数多
  var option={
      chart: {
        renderTo: '',
        type: 'line',
        shadow: true,
        marginRight: 15
      },
      title: {
        text: '数据曲线图表',
        x: -20 //center
      },
      xAxis:{
        type:'datetime'
      },
      yAxis:{
        title: {
          text: '数据'
        }
        /*tickInterval:10,//纵坐标的间隔
        max:80, //高出100的数值为错误数据
        plotBands: [{ // mark the weekend
                color: '#dd4b39',
                from:70,
                to:80
            }],
        min:20*/
      },
      tooltip:{
        xDateFormat:'%Y-%m-%d %H:%M:%S',
        borderColor: 'green',
        borderWidth:1
      },
      legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                borderWidth: 0
      },
      series:  [{
        name: '',
        data: []
          }]
      };

  $("#nav-collect").click(function(){
    //点击实时采集时初始化应力传感器图
    drawchart();
  });
  //var php_json = <?=$php_json?>; 
  //点击二级tab后异步操作-画图
  $("#secondaryTab li").click(function(){
      sensor_type=$(this).attr("id");
      sensor_sort_num=$(this).attr("value");
      drawchart();
     });

  //点击查看详情
  var box = new Box("#idBox");
  $(".sensor_pic+button").click(function(){
      id=$(this).attr("value");
      box.show();
      $.ajax({
        url: "",
        dataType : 'html',
        data:{
          bridge_id:bridge_id,
          sensor_id:id},
        success: function(data) {
          $("#result").html(data);
        },
        error:function(){alert("传感器数据读取错误！");}
      });    
    });
  $("#boxCancel").click(function(){
    box.close();
  });

  $("#nav-analyse").click(function(){
    analyse();
  });
  $("#analyse_table_btn").click(function(){
    $("#analyse_table").show();
    $("#analyse_chart").hide();
  });
  $("#analyse_pic_btn").click(function(){
    $("#analyse_table").hide();
    $("#analyse_chart").show();
  });

  $('#analyse_choose').change(function(){
    analyse_type=$(this).val();
    analyse_sensor_sort_num=$(this).find("option:selected").attr("analyse-num");
    analyse();
  });
  $('#analyse_time').change(function(event) {
    /* Act on the event */
    analyse_time=$(this).val();
    analyse();
  });
  $("#analyse_data_choose").change(function(){
        analyse_data_type=$(this).val();
        $.post('',
            {bridge_id:bridge_id,
             sensor_model:analyse_data_type},
           function(data) {
             $("#showDataTable").empty().html(data);
         });
      });

  function drawchart() {
    //异步式的读取数据,实时监控
    $.ajax({
        url: "",
        type:"POST",
        dataType : 'json',
        data:{sensor_type:sensor_type,
              bridge_id:bridge_id},
        success: function(data) {
          message = eval('(' +data+ ')');/*解析JSON*/
          //数据读取成功后画图。是个JSON
          for(var i=0;i<sensor_sort_num;i++){
            var id=message[i].id;
            //将mysql中的时间只精确到秒。而js中要求精确到毫秒。/在Date.UTC方法中月份要减一            
            for(var j=0;j<message[i].data.length;j++){
              var time=new Array();
              time=message[i].data[j][0].split(",");
              message[i].data[j][0]=Date.UTC(time[0],time[1]-1,time[2],time[3],time[4],time[5],time[6]);
            }
            option.series[0].name="传感器"+id;
            option.series[0].data=message[i].data;
            option.chart.renderTo =sensor_type+"_"+id;
            //阻止用户因多次点击标签后会启动多个定时器，引起同一图多次刷新
            if(!chart[id]){
              chart[id]=new Highcharts.Chart(option);
              //setTimeout(refreshData,4000,id);
            }
            //chart[id]=new Highcharts.Chart(option);
          }
        },
        error:function(){alert("传感器数据读取错误！");}
    });
  }
  function refreshData(id){
    $.ajax({
        url:"",
        type:"POST",
        dataType : 'json',
        data:{sensor_id:id,
              bridge_id:bridge_id},
        success: function(data) {
          series=chart[id].series[0];
          shift=series.data.length>9;//最多显示9个数
          var time=new Array();
          time=data[0].split(",");
          data[0]=Date.UTC(time[0],time[1]-1,time[2],time[3],time[4],time[5],time[6]);
          
          chart[id].series[0].addPoint(data,true,shift);
          //setTimeout(refreshData,4000,id);
        },
        cache: false,
        error:function(){alert("数据更新错误！");}
    });
  }

  function analyse(){ 	
    $("#analyse_math thead").nextAll().empty();
    var analyse_chart;
    var analyse_option={
      chart:{
        renderTo:"analyse_container",
        shadow: true,
        marginRight:45,
        marginLeft:10,
        marginTop:20,
        width: 1070,
        hight: 900
      },
      tooltip: {
        xDateFormat:'%Y-%m-%d %H:%M:%S',
        borderColor: 'green',
        borderWidth:1
      },
      rangeSelector: {
            buttons: [{
                type: 'day',
                count: 1,
                text: '一天'
            }, {
                type: 'day',
                count: 7,
                text: '一周'
            }, {
                type: 'month',
                count: 1,
                text: '一月'
            }, {
                type: 'all',
                text: 'All'
            }],
            selected: 0
      },
      legend: {
        enabled: true,
        shadow: true
      },
      xAxis:{
        type:'datetime'
      },
      series: [{}]
    };
    $.ajax({
      url: '',
      type: 'POST',
      dataType: 'json',
      data: {sensor_type:analyse_type,
              time:analyse_time,
              bridge_id:bridge_id},
      success: function(data){
        message = eval('(' +data+ ')');
        alert(data);
        if(!message) {
          analyse_chart=new Highcharts.StockChart(analyse_option);
        }
        for(var i=0;i<analyse_sensor_sort_num;i++){
            var id=message[i].id;
            name_temp="传感器"+id;
            data_temp=message[i].data;
            $("#analyse_math").append("<tr><td>"+id+"</td><td>"+message[i].max+"</td><td>"+message[i].min+"</td><td>"+message[i].num+"</td><td>"+message[i].s+"</td></tr>");
            //时间戳转换为ms的datetime
            for(var j=0;j<data_temp.length;j++){
              var time=new Array();
              time=data_temp[j][0].split(",");
              data_temp[j][0]=Date.UTC(time[0],time[1]-1,time[2],time[3],time[4],time[5],time[6]);
            }
            if(!analyse_chart){
              analyse_option.series[0].name=name_temp;
              analyse_option.series[0].data=data_temp;
              analyse_chart=new Highcharts.StockChart(analyse_option);
            }else{
              analyse_chart.addSeries({
                name:name_temp,
                data:data_temp
              });
            }
          }

      },
      error:function(){alert("传感器数据读取错误！");}
    });
  }

 });