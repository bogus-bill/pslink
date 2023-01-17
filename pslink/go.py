#!/usr/bin/env python3

sql = """select
  p.ref_id as process_uuid,
  p.name  as process_name,
  l.code as process_location,
  f.ref_id as flow_uuid,
  f.name   as flow_name,
  u.name   as unit
  from tbl_processes p
  inner join tbl_exchanges e on p.id = e.f_owner
  inner join tbl_flows f on e.f_flow = f.id
  inner join tbl_units u on e.f_unit = u.id
  inner join tbl_locations l on p.f_location = l.id
  where f.flow_type = 'PRODUCT_FLOW'
    and e.is_input  = 0
    and u.name      = 'kg'
"""

from pslink import backs, semap, symap

graph = semap.read_file("data/product_net.semapl")
products = backs.read_products("/mnt/c/Users/Elias/Desktop/flows_sql.txt")
graph.link_products(products)

txt = "Polypropylene, PP, granulate"

[a.as_dict() for a in graph.find_products(txt)]
