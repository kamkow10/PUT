unit armstrong_unit1;

{$mode objfpc}{$H+}

interface

uses
  Classes, Math, SysUtils, FileUtil, Forms, Controls, Graphics, Dialogs,
  StdCtrls, ExtCtrls;

type

  { TTWyszukiwarka }

  TTWyszukiwarka = class(TForm)
    Image1: TImage;
    Label1: TLabel;
    Twyszukaj: TButton;
    Tmax: TEdit;
    Tarmstrong: TMemo;
    procedure Button1Click(Sender: TObject);
    procedure Image1Click(Sender: TObject);
  private
    { private declarations }
  public
    { public declarations }
  end;

var
  TWyszukiwarka                     : TTWyszukiwarka;
  cyfry, max, liczba, krok  : integer;
  sum                       : extended;

  function ilosc_cyfr : extended;
  function suma_cyfr(p : extended) : extended ;

implementation

{$R *.lfm}

function ilosc_cyfr : extended;                     {Funkcja sprawdzająca
                                                       ilosc cyfr}
var
a     : integer;

  begin
  a := liczba;
  cyfry := 1;
  while a div 10 > 0 do
      begin
        Inc(cyfry);
        a:=a div 10;
      end;
  result := cyfry;
  end;

function suma_cyfr(p : extended) : extended ;       {Funkcja licząca sumę
                                                     spotęgowanych cyfr liczby}
var
cyfra, b      : integer;
potega_cyfry  : extended;

  begin
  b := liczba;
  sum := 0;
   while b > 0 do
      begin
          cyfra := b mod 10;
          potega_cyfry := power(cyfra, p);
          sum := sum + potega_cyfry;
          b := b div 10;
      end;
  result := sum;
  end;

{ TTWyszukiwarka }

procedure TTWyszukiwarka.Button1Click(Sender: TObject);
begin
liczba:=1;
Tarmstrong.Clear;
 try
    for krok := 1 to strtoint(Tmax.Text) do
      begin
        if suma_cyfr(ilosc_cyfr) = liczba then
            begin
              Tarmstrong.SelText:= inttostr(liczba) + '  ';
            end;
        Inc(liczba);
      end;
 except
    Showmessage('Podano zlą liczbę');
 end;

end;

procedure TTWyszukiwarka.Image1Click(Sender: TObject);
begin

end;

end.

