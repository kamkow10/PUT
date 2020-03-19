program Domowa_wypo¿yczalnia_ksi¹zek;

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
