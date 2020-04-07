#ifndef CaloCellMerge_h
#define CaloCellMerge_h

#include "CaloRecTool.h"
#include "GaugiKernel/Algorithm.h"
#include "GaugiKernel/DataHandle.h"
#include "CaloCell/CaloCell.h"
#include "CaloCellCollection.h"


class CaloCellMerge : public Gaugi::Algorithm
{
  public:
  
    /** Contructor **/
    CaloCellMerge( std::string name );
    /** Destructor **/
    ~CaloCellMerge();
    
    /*! initialize the algorithm **/
    virtual StatusCode initialize() override;
    /*! Execute in step action step from geant core **/
    virtual StatusCode execute( SG::EventContext &ctx , const G4Step *step) const override;
    /*! execute before start the step action **/
    virtual StatusCode pre_execute( SG::EventContext &ctx ) const override;
    /*! execute after the step action **/ 
    virtual StatusCode post_execute( SG::EventContext &ctx ) const override;
    /*! fill hisogram in the end **/
    virtual StatusCode fillHistograms( SG::EventContext &ctx ) const override;
    /*! finalize the algorithm **/ 
    virtual StatusCode finalize() override;

  private:
    
    /*! collection key */
    std::vector<std::string> m_collectionKeys;
    /*! CaloCellContainer key for reco cells */
    std::string m_cellsKey;
    /*! CaloCellContainer key for truth cells */
    std::string m_truthCellsKey;
};



#endif