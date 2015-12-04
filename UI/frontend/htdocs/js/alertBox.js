//点击查看详情，覆盖层、高亮层
    var isIE = (document.all) ? true:false;

    var Factory = {
                create:function(){
                    return function(){
                        this.initialize.apply(this,arguments);
                    };
                }
            }
    var Overlay=Factory.create();
    Overlay.prototype={
      initialize:function(){
        this.setOptions();
        this.lay = $("<div>").insertBefore("body");
        this.color=this.options.color;
        this.opacity = parseInt(this.options.opacity);
        this.zIndex = parseInt(this.options.zIndex);
        this.lay.css({"display":"none","zIndex":this.zIndex,"left":"0","top":"0","position":"fixed","width":"100%","height":"100%"});
      },
      setOptions:function(){
        this.options={
           //lay: null,
          color: "#000",
          opacity: 50,
          zIndex:1000
        }
      },
      show:function(){                    
        isIE ? this.lay.css("filter","alpha(opacity:" + this.opacity + ")") : this.lay.css("opacity",this.opacity / 100);
        this.lay.css({"backgroundColor":this.color,"display":"block"});
                },
      close:function(){
                this.lay.css("display","none");
                }
      }
    var Box = Factory.create();
    Box.prototype = {
                initialize:function(box){
                    this.box=$(box);
                    this.myOverlay = new Overlay();
                    this.setOptions();
                    this.zIndex = this.myOverlay.zIndex+1;
                    this.height = this.box.innerHeight();
                    this.width = this.box.innerWidth();
                    this.Over=!!this.options.Over;
                    this.Fixed = !!this.options.Fixed;
                    this.Center = !!this.options.Center;
                    this.box.css({"zIndex":this.zIndex,"display":"none"});                    
                },
                setOptions:function(){
                        this.options={
                            Over:true,
                            Fixed:true,
                            Center:false
                        }
                }    ,
                setCenter:function(){
                    //注意这里获得scrollTop所选择的对象
                    this.box.css({"margin-top":$(document).scrollTop()-this.height/2,"margin-left":$(document).scrollLeft()-this.width/2})
                },
                show:function(){
                    this.box.css("position",this.Fixed?"fixed":"absolute");
                    this.Over&&this.myOverlay.show();
                    if(this.Center)
                    {
                        this.box.css({"top":"50%","left":"50%"});
                        this.setCenter();
                    }
                    this.box.css("display","block");
                },
                close:function(){
                    this.box.css("display","none");
                    this.myOverlay.close();
                }
            }