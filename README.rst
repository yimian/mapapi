mapapi
-----------------

通过调用第三方地图接口, 处理与地图相关应用. 目前仅支持百度地图, 期待支持更多地图应用.

使用方法:

- 获取地址地理坐标

  >>> from mapapi import baidu
  >>> map_api = baidu.MapApi(['your application key', ...])
  >>> location = map_api.location_api.get_location_by_address(u'百度大厦', u'北京')
  >>> print location


- 获取地理坐标对应的详细地址

  >>> from mapapi import baidu
  >>> map_api = baidu.MapApi(['your application key', ...])
  >>> address = map_api.location_api.get_address_by_location({'lng': 116.322987, 'lat': 39.983424})
  >>> print address


- 获取标准化地址信息

  >>> from mapapi import baidu
  >>> map_api = baidu.MapApi(['your application key', ...])
  >>> address = map_api.location_api.get_formatted_address(u'北京市海淀区百度大厦')
  >>> print address


- 通过关键词查询所有地名或店铺等信息

  >>> from mapapi import baidu
  >>> map_api = baidu.MapApi(['your application key', ...])
  >>> ret = map_api.place_api.get_place_all(u'银行', u'济南')
  >>> print ret

- 通过百度地图uid信息获取对应的地址信息

  >>> from mapapi import baidu
  >>> map_api = baidu.MapApi(['your application key', ...])
  >>> place = map_api.place_api.get_place_by_uids('c14fc238f7fadd4ea5da390f')
  >>> print place

- 将腾讯地图坐标转换成百度地图坐标

  >>> from mapapi import baidu
  >>> map_api = baidu.MapApi(['your application key', ...])
  >>> coords = map_api.transform_api.transform({'lat': 29.5754297789, 'lng': 114.218927345})
  >>> print coords


安装方法:

  pip install mapapi
