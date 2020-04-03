#ifndef EventAction_h
#define EventAction_h

/** geant 4 includes **/
#include "G4UserEventAction.hh"
#include "globals.hh"


class EventAction : public G4UserEventAction
{
  public:
    EventAction();
    virtual ~EventAction();

    virtual void  BeginOfEventAction(const G4Event* event);
    virtual void    EndOfEventAction(const G4Event* event);
    
};
                     

#endif

    
