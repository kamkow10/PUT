program Domowa_wypożyczalnia_ksiązek;

uses
  System.StartUpCopy,
  FMX.Forms,
  Unit1 in 'Unit1.pas' {Twypozyczalnia};

{$R *.res}

begin
  Application.Initialize;
  Application.CreateForm(TTwypozyczalnia, Twypozyczalnia);
  Application.Run;
end.
