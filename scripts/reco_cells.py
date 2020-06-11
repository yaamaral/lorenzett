#!/usr/bin/env python3

from Gaugi.messenger    import LoggingLevel, Logger
from Gaugi              import GeV
from PythiaGenerator    import EventReader
from G4Kernel           import *
from CaloRec            import RawNtupleMaker
import numpy as np
import argparse
import sys,os


mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-i','--inputFile', action='store', dest='inputFile', required = False,
                    help = "The event input file generated by the Pythia event generator.")

parser.add_argument('-o','--outputFile', action='store', dest='outputFile', required = False,
                    help = "The reconstructed event file generated by lzt/geant4 framework.")

parser.add_argument('--outputLevel', action='store', dest='outputLevel', required = False, type=int, default=1,
                    help = "The output level messenger.")

parser.add_argument('-nt','--numberOfThreads', action='store', dest='numberOfThreads', required = False, type=int, default=1,
                    help = "The number of threads")

parser.add_argument('--evt','--numberOfEvents', action='store', dest='numberOfEvents', required = False, type=int, default=None,
                    help = "The number of events to apply the reconstruction.")

parser.add_argument('--visualization', action='store_true', dest='visualization', required = False,
                    help = "Run with Qt interface.")

parser.add_argument('--cal','--calorimeter', action='store', dest='Calorimeter', required = False,
                    help = "Choose the calorimeter")

if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()


# Get all output names
if not '.root' in args.outputFile:
  args.outputFile+='.root'

# Add index for each thread
outputFileList = []
for thread in range( args.numberOfThreads ):
  outputFileList.append( args.outputFile.replace( '.root', "_%d.root"%thread ) )


from DetectorATLASModel import DetectorConstruction as ATLAS
from DetectorGenericModel import DetectorConstruction as Generic
from DetectorATLASModel import CaloCellBuilder


if args.Calorimeter == "ATLAS":
    
    from DetectorATLASModel import CaloCellBuilder
        
    acc = ComponentAccumulator("ComponentAccumulator",
                              ATLAS("GenericATLASDetector"),
                              RunVis=args.visualization,
                              NumberOfThreads = args.numberOfThreads,
                              OutputFile = args.outputFile)

if args.Calorimeter == "Generic":
    
    from DetectorGenericModel import CaloCellBuilder
        
    acc = ComponentAccumulator("ComponentAccumulator",
                              Generic("GenericATLASDetector"),
                              RunVis=args.visualization,
                              NumberOfThreads = args.numberOfThreads,
                              OutputFile = args.outputFile)

if args.Calorimeter == "Scintillator":
    
    from DetectorScintiModel import CaloCellBuilder
        
    acc = ComponentAccumulator("ComponentAccumulator",
                              Scinti("ScintiDetector"),
                              RunVis=args.visualization,
                              NumberOfThreads = args.numberOfThreads,
                              OutputFile = args.outputFile)





gun = EventReader( "PythiaGenerator",
                   EventKey   = recordable("EventInfo"),
                   FileName   = args.inputFile)



calorimeter = CaloCellBuilder("CaloCellATLASBuilder",
                              HistogramPath = "Expert/CaloCells",
                              OutputLevel   = args.outputLevel)




raw = RawNtupleMaker (  "RawNtupleMaker",
                        EventKey        = recordable("EventInfo"),
                        CellsKey        = recordable("Cells"),
                        EtaWindow       = 0.4,
                        PhiWindow       = 0.4,
                        OutputLevel     = args.outputLevel)

gun.merge(acc)
calorimeter.merge(acc)
acc += raw
acc.run(args.numberOfEvents)




# Merge all files
command = "hadd -f " + args.outputFile + ' '
for fname in outputFileList:
  command+=fname + ' '
print( command )
os.system(command)

# remove thread files
for fname in outputFileList:
  os.system( 'rm '+ fname )





