FUNCTION_BLOCK MotorControl
VAR_INPUT
    StartButton : BOOL;    // Signal för att starta motorn
    StopButton  : BOOL;    // Signal för att stoppa motorn (Normalt stängd)
    Emergency   : BOOL;    // Nödstopp (TRUE = OK, FALSE = STOPP)
END_VAR

VAR_OUTPUT
    MotorActive : BOOL;    // Status om motorn går
    Fault       : BOOL;    // Indikerar fel om nödstopp är aktivt
END_VAR

VAR
    RunLatch    : BOOL;    // Intern hållkrets
    Timer       : TON;     // Timer för att logga drifttid
END_VAR

// --- LOGIK START ---

// Hållkrets för start/stopp med prioritet på stopp
IF NOT Emergency THEN
    RunLatch := FALSE;
    Fault := TRUE;
ELSIF StopButton THEN
    RunLatch := FALSE;
    Fault := FALSE;
ELSIF StartButton THEN
    RunLatch := TRUE;
    Fault := FALSE;
END_IF;

// Tilldela utgången
MotorActive := RunLatch;

// Exempel på timer: Räkna hur länge motorn varit aktiv (PT på 10 sekunder)
Timer(IN := MotorActive, PT := T#10s);

// --- LOGIK SLUT ---
END_FUNCTION_BLOCK
