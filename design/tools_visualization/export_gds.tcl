# magic: export named cells from mag/ to GDS, ready for the layer dump.
#
#   cd mag && magic -dnull -noconsole ../tools_visualization/export_gds.tcl
#
# Cells and destination come from the environment so the shell driver can set them:
#   VIZ_CELLS  space-separated cell names   (default: the soma + synapse pair)
#   VIZ_OUT    directory to write .gds into (default: ./build)

set cells [expr {[info exists env(VIZ_CELLS)] ? $env(VIZ_CELLS) \
                 : "lif4syn_fed_v1 dpi_syn_v1_4bitsFF"}]
set out   [expr {[info exists env(VIZ_OUT)]   ? $env(VIZ_OUT)   : "./build"}]
file mkdir $out

gds rescale false
foreach c $cells {
    if {[catch {load $c} err]} {
        puts stderr "SKIP $c: $err"
        continue
    }
    select top cell
    gds write $out/$c.gds
    puts "WROTE $out/$c.gds"
}
quit -noprompt
