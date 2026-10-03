proc ext_lvs {name} {
  load $name
  select top cell
  extract path extfiles
  extract all
  ext2spice lvs
  ext2spice -p extfiles -o "spicefiles/${name}.spice"
}

proc ext_pex {name} {
  load $name
  flatten "${name}_pex"
  load "${name}_pex"
  select top cell
  extract path extfiles
  extract all
  ext2sim labels on
  ext2sim -p extfiles
  ext2spice lvs
  ext2spice cthresh 0
  ext2spice -p extfiles -o "spicefiles/${name}_pex.spice"
}

proc ext_rcx {name} {
  load $name
  flatten "${name}_rcx"
  load "${name}_rcx"
  select top cell
  extract path extfiles
  extract all
  ext2sim labels on
  ext2sim -p extfiles
  extresist tolerance 10
  extresist
  ext2spice lvs
  ext2spice cthresh 0
  ext2spice extresist on
  ext2spice -p extfiles -o "spicefiles/${name}_rcx.spice"
}

proc check_antenna {name} {
  ext_lvs $name

  antennacheck debug
  antennacheck extfiles/${name}

  puts "Antenna violation count: [feedback count]"
}
