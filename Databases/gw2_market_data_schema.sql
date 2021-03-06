CREATE TABLE Recipes (
    recID           INTEGER PRIMARY KEY
                            NOT NULL,
    itmID           INTEGER NOT NULL,
    count           INTEGER NOT NULL,
    components      STRING  NOT NULL,
    craftTime       INTEGER NOT NULL,
    byArtificer     BOOLEAN NOT NULL,
    byArmorsmith    BOOLEAN NOT NULL,
    byChef          BOOLEAN NOT NULL,
    byHuntsman      BOOLEAN NOT NULL,
    byJeweler       BOOLEAN NOT NULL,
    byLeatherworker BOOLEAN NOT NULL,
    byTailor        BOOLEAN NOT NULL,
    byWeaponsmith   BOOLEAN NOT NULL,
    byScribe        BOOLEAN NOT NULL
);

CREATE TABLE Items (
    itmID     INTEGER PRIMARY KEY
                      NOT NULL,
    name      STRING  NOT NULL,
    icon      TEXT    NOT NULL,
    sellable  BOOLEAN NOT NULL,
    craftable BOOLEAN NOT NULL
);

CREATE TABLE Market (
    time     TIME    NOT NULL,
    itmID    INTEGER NOT NULL,
    buy_prc  INTEGER NOT NULL,
    buy_amt  INTEGER NOT NULL,
    sell_prc INTEGER NOT NULL,
    sell_amt INTEGER NOT NULL,
    PRIMARY KEY (
        time,
        itmID
    )
);
