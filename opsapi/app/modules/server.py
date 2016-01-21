#_*_coding:utf-8_*_
from app.models import db, Server
from app.utils import check_field_exists,process_result
import inspect

def create(**params):
    # 1. 获取参数信息
    check_field_exists(Server, params)

    print inspect.getmembers(Server,predicate=inspect.ismethod(id))

    # 传参的个数需要验证
    obj = Server(**params)

    # 插入到数据库
    db.session.add(obj)
    db.session.commit()
    return obj.id

def get(**params):
    output = params.get('output',[])
    limit = params.get('limit',10)
    order_by = params.get('order_by','id desc')

    data = db.session.query(Server).order_by(order_by).limit(limit).all()
    db.session.close()

    ret = process_result(data, output)
    return ret

def update(**params):
    data = params.get('data',{})
    where = params.get('where',{})

    if not data:
        raise Exception("没有需要的no data")

    for field in data.keys():
        if not hasattr(Server,field):
            raise Exception("需要更新的{}这个字段不存在 no{}")

    if not where:
        raise Exception("需要提供where条件 no where")

    if where.get('id', None) is None :
        raise Exception("需要提供id 作为条件 no con")

    try:
        id = int(where['id'])
        if id <= 0:
            raise Exception("条件id的值不能为负数  id")
    except ValueError:
        raise Exception("条件id的值必须为int  ")

    ret = db.session.query(Server).filter_by(**where).update(data)
    db.session.commit()

    return ret