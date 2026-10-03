# klayout -b -r dump_layers.rb
#
# Reads one GDS and writes the flattened, merged geometry of every drawn layer
# as JSON. Each polygon is decomposed into trapezoids first: they are convex
# quads, so the renderer can extrude them with holes pre-resolved.
#
#   VIZ_CELL  basename of the .gds to read and the .json to write
#   VIZ_OUT   directory holding both (default: ./build)

require 'json'

name = ENV["VIZ_CELL"] or abort "set VIZ_CELL"
dir  = ENV["VIZ_OUT"] || "./build"

ly = RBA::Layout::new
ly.read("#{dir}/#{name}.gds")
top = ly.top_cells[0]
dbu = ly.dbu

bb  = top.bbox
out = {
  "cell"   => name,
  "dbu"    => dbu,
  "bbox"   => [bb.left*dbu, bb.bottom*dbu, bb.right*dbu, bb.top*dbu],
  "layers" => {},
}

ly.layer_indexes.each do |li|
  info = ly.get_info(li)
  reg  = RBA::Region::new(top.begin_shapes_rec(li))
  reg.merge
  next if reg.count == 0

  quads = []
  reg.each do |poly|
    poly.decompose_trapezoids(RBA::Polygon::TD_simple).each do |t|
      pts = t.each_point.map { |p| [(p.x*dbu).round(4), (p.y*dbu).round(4)] }
      quads << pts if pts.size >= 3
    end
  end
  out["layers"]["#{info.layer}/#{info.datatype}"] = quads
end

File.write("#{dir}/#{name}.json", JSON.generate(out))
puts "WROTE #{dir}/#{name}.json  layers=#{out['layers'].size} " \
     "quads=#{out['layers'].values.map(&:size).sum}"
