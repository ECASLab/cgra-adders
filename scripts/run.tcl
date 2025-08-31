#-----------------------------------------------------------------------------
# Title       : Synthesis Automation Script
# File        : run.tcl
# Date        : 2025-06-04
# Author      : Erick Andrés Obregón Fonseca
# Email       : erickof@ieee.org
# Organization: ECASLAB
# Description : Automates the synthesis of parameterized adders using Synopsys
#               Design Compiler. Generates area, power, and timing reports for
#               multiple architectures and bit widths.
# License     : MIT License (see LICENSE file for details)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Procedure: mkdir_parent
# Description: Deletes a directory if it exists, then creates a fresh one.
#-----------------------------------------------------------------------------
proc mkdir_parent {dir} {
  if {[file exists $dir]} {
    file delete -force $dir
  }

  file mkdir $dir
}

#-----------------------------------------------------------------------------
# Procedure: create_directories
# Description: Loops over a list of directories and recreates each one
#              cleanly.
#-----------------------------------------------------------------------------
proc create_directories {dirs} {
  foreach dir $dirs {
    mkdir_parent $dir
  }
}

#-----------------------------------------------------------------------------
# Procedure: generate_verilog_with_parameter
# Description: Reads a Verilog template, replaces "N = <value>" with a new
#              value, and writes it to a new file.
# Arguments:
#   - template_file: input template path.
#   - output_file: output file path.
#   - value: value to substitute for N.
#-----------------------------------------------------------------------------
proc generate_verilog_with_parameter {template_file output_file value} {
  # Read the input template file
  set file_in [open $template_file r]
  set content [read $file_in]
  close $file_in

  # Replace all instances of N = <number> with N = $value
  regsub -all {N\s*=\s*[0-9]+} $content "N = $value" result

  # Write the modified content to the output file
  set file_out [open $output_file w]
  puts $file_out $result
  close $file_out
}

#-----------------------------------------------------------------------------
# Create all necessary output directories
#-----------------------------------------------------------------------------
create_directories {ddc reports sdf synth tmp}

#-----------------------------------------------------------------------------
# Load environment configuration and libraries
#-----------------------------------------------------------------------------
set search_path    "models tmp"
set target_library $env(TARGET_LIBRARY)
set link_library   $env(TARGET_LIBRARY)

# Load adder types and bit-widths from environment
set adders          $env(ADDERS)
set building_blocks $env(BUILDING_BLOCKS)
set bit_width       $env(BIT_WIDTHS)

# Copy shared include modules to working directory
set src_dir     "src/rtl"
set include_dir "$src_dir/include"

#-----------------------------------------------------------------------------
# Main synthesis loop over all (adder, bit_width) pairs
#-----------------------------------------------------------------------------
foreach adder $adders building_block $building_blocks {
  foreach bits $bit_width {
    set adder_name        $adder$bits
    set verilog_tmp_name "${adder_name}_tmp.v"

    puts "Processing $adder with $bits bits"

    file copy -force $include_dir/${building_block}.v tmp/${building_block}.v

    # Generate bit-width-specific Verilog file from template
    generate_verilog_with_parameter "$src_dir/$adder/${adder}.v" \
                                    "tmp/${verilog_tmp_name}" \
                                    $bits

    # Read generated Verilog into Design Compiler
    read_verilog ${verilog_tmp_name}

    # Set the top-level module
    current_design $adder

    # Link the design and build internal netlist
    link

    # Ensure the design library is initialized
    define_design_lib WORK -path ./WORK

    # Protect reusable components from being optimized away
    set_dont_touch         [get_designs $building_block]
    set_dont_touch_network [get_designs $building_block]

    # Run synthesis with aggressive optimization
    compile_ultra

    # Save synthesis outputs
    write -format ddc     -hierarchy -output "ddc/${adder_name}.ddc"
    write -format verilog -hierarchy -output "synth/${adder_name}_synth.v"
    write_sdf "sdf/${adder_name}.sdf"

    # Generate design reports
    report_area   > "reports/${adder_name}_area.rpt"
    report_power  > "reports/${adder_name}_power.rpt"
    report_timing > "reports/${adder_name}_timing.rpt"

    puts "Finished processing $adder with $bits bits"
    puts "----------------------------------------"

    # Clean up before next iteration
    remove_design -all
  }
}

# Exit the tool after synthesis
exit
