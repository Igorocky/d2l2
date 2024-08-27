create table TRAIN_LOG
(
    id            integer primary key,
    ask_at        integer not null,
    ask_at_str    text    not null,
    ask_clef      text    not null check ( ask_clef in ('B', 'T') ),
    ask_note      integer not null check ( 0 <= ask_note and ask_note <= 87 ),
    ask_note_name text    not null,
    ans_at        integer not null,
    ans_note      integer not null,
    ans_note_name text    not null
) strict;