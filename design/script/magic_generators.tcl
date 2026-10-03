# Generate standard cell (hd) power rails for width x height units at current cursor
#
proc generate_digital_rails {{width 1} {height 1}} {
    snap internal

    pushbox
    generate_rail_m1li

    box move n 2.72um
    generate_rail_m1li

    peekbox
    box size 0.46um 3.2um
    select area
    box size 0.46um 2.72um
    array $width $height
    popbox
}

# Generate analog cell power rails for width units at current cursor
#
# The optional second argument controls the width of the midrail
#   default:   same as the total power rail width
#   0:         midrail generation off
#   otherwise: width specified by the argument
#   
proc generate_analog_rails {width {midrailwidth -1}} {
    snap internal
    pushbox

    # SC rail bottom
    generate_rail_m1li

    # GND with tap
    box move n 0.96um
    generate_rail_m1liptap

    # AVDD
    peekbox
    box move n 7.2um
    generate_rail_m1li

    # GNDtap
    peekbox
    box move n 8.160um
    generate_rail_m1liptap

    # SC rail top
    peekbox
    box move n 9.920um
    generate_rail_m1li

    peekbox
    box size 0.46um 10.4um
    select area
    array $width 1

    # optionally add midrail, just m1
    if {$midrailwidth == -1} {
        set midrailwidth $width
    }
    if {$midrailwidth != 0} {
        peekbox
        box move n 4.080um
        box size 0.460um 0.480um
        paint m1

        select area
        array $midrailwidth 1
    }

    select clear
    popbox
}

##
# Helpers for drawing power rail tiles
#
# generate_rail_m1li:      draws on m1 and li
# generate_rail_m1liptap:  draws on m1, li, and ptap
#
proc generate_rail_m1li {} {
    snap internal
    pushbox

    box size 0.46um 0.48um
    paint m1
    box move n 0.155um
    box height 0.17um
    paint li
    box move e 0.145um
    box width 0.17um
    paint mcon
    popbox
}

proc generate_rail_m1liptap {} {
    snap internal
    pushbox

    box size 0.46um 0.48um
    paint m1
    box move n 0.155um
    box height 0.17um
    paint li
    paint ptap
    box move e 0.145um
    box width 0.17um
    paint mcon
    paint ptapc

    popbox
}

