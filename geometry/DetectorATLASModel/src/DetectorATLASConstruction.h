#ifndef DetectorATLASConstruction_h
#define DetectorATLASConstruction_h

#include "GaugiKernel/MsgStream.h"
#include "G4VUserDetectorConstruction.hh"
#include "G4Material.hh"
#include "G4ThreeVector.hh"
#include "G4Region.hh"
#include "globals.hh"


class G4VPhysicalVolume;
class G4GlobalMagFieldMessenger;


class DetectorATLASConstruction : public G4VUserDetectorConstruction, public MsgService
{
  public:
    DetectorATLASConstruction(std::string);
    virtual ~DetectorATLASConstruction();
    virtual G4VPhysicalVolume* Construct();
    virtual void ConstructSDandField();

    // get methods
    const G4VPhysicalVolume* GetAbsorberPV() const;
    const G4VPhysicalVolume* GetGapPV() const;
     
  private:

    // methods
    void DefineMaterials();
    
    G4VPhysicalVolume* DefineVolumes();


    void CreateBarrel(  G4LogicalVolume *worldLV, 
                        std::string name,  
                        G4Material *defaltMaterial,
                        G4Material *absorberMaterial,
                        G4Material *gapMaterial,
                        int nofLayers,
                        double absoThickness,
                        double gapThickness,
                        double calorRmin,
                        double calorZ,
                        G4ThreeVector center_pos,
                        G4Region* region);


    static G4ThreadLocal G4GlobalMagFieldMessenger*  m_magFieldMessenger; // magnetic field messenger
    bool m_checkOverlaps; // option to activate checking of volumes overlaps
};




#endif

