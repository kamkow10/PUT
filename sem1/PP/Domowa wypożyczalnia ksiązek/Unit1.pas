unit Unit1;

interface

uses
  System.SysUtils, System.Types, System.UITypes, System.Classes, System.Variants,
  FMX.Types, FMX.Controls, FMX.Forms, FMX.Graphics, FMX.Dialogs, FMX.StdCtrls,
  FMX.Controls.Presentation, FMX.Edit, FMX.Layouts, FMX.ListBox, FMX.Objects;

type
  TTwypozyczalnia = class(TForm)
    Tlista: TListBox;
    Ttytul_zapisz: TEdit;
    Twypo_zapisz: TEdit;
    Tautor_zapisz: TEdit;
    Tdodaj: TButton;
    Todczyt: TButton;
    Tdata_zapisz: TEdit;
    Tusun: TButton;
    Ttytul_zmien: TEdit;
    Twypo_zmien: TEdit;
    Tautor_zmien: TEdit;
    Tdata_zmien: TEdit;
    Tzmien: TButton;
    Tsortuj: TButton;
    Tautor_wyszukaj: TEdit;
    Twypo_wyszukaj: TEdit;
    Tod: TEdit;
    Tdo: TEdit;
    Twyszukaj: TButton;
    Twyszukaj2: TButton;
    Twyszukaj3: TButton;
    Tzapisz: TButton;
    Twczytaj: TButton;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Image1: TImage;
    Image2: TImage;
    Tskopiuj: TButton;
    Label6: TLabel;
    Label7: TLabel;
    Label8: TLabel;
    Tczysc: TButton;
    Image3: TImage;
    procedure TdodajClick(Sender: TObject);
    procedure TodczytClick(Sender: TObject);
    procedure TusunClick(Sender: TObject);
    procedure TzmienClick(Sender: TObject);
    procedure TsortujClick(Sender: TObject);
    procedure TwyszukajClick(Sender: TObject);
    procedure Twyszukaj2Click(Sender: TObject);
    procedure Twyszukaj3Click(Sender: TObject);
    procedure TwczytajClick(Sender: TObject);
    procedure TzapiszClick(Sender: TObject);
    procedure TskopiujClick(Sender: TObject);
    procedure TczyscClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

type
{wskaŸnik na element listy}
  wskaznik = ^element;

{rekord przechowuj¹cy informacje o wypo¿yczonej ksi¹¿ce }
  book = record
     autor : string[50];  // autor
     tytul : string[50];  // tytu³
     wypo : string[50];   // osoba wypo¿yczaj¹ca
     data : TDateTime;  // data wypo¿yczenia
    end;

{element listy}
  element = record
     dane : book;   //  informacje o wypo¿yczonej ksi¹¿ce
     next : wskaznik;  // wskaŸnik na nastêpny element listy
    end;

  plik = file of book;  // deklaracja pliku typowanego


var
  Twypozyczalnia: TTwypozyczalnia;
  L : wskaznik; // wskaŸnik na pocz¹tek listy
  fp : plik; // zmienna typu plik
Const
  FileName = 'Dane.dat';  // sta³a przechowuj¹ca nazwê pliku

implementation

{$R *.fmx}

{procedura dodaj¹ca element do listy}
procedure dodaj (var head : wskaznik; x : string; y : string;
                  z : string; t : tdatetime);
var
  e : wskaznik; // nowy element listy
  p : wskaznik; // wskazŸnik pomocniczy
begin
  New(e);
  e^.next := nil;
{przypisanie wartoœci parametrów x, y, z, t do rekordu}
  e^.dane.autor := x;
  e^.dane.tytul := y;
  e^.dane.wypo := z;
  e^.dane.data := t;

  p := head;
  if p = nil then
    head := e
  else
  begin
    while p^.next <> nil do // pêtla przesuwaj¹ca wskaznik na koniec listy
    begin
      p := p^.next;
    end;
    p^.next := e;
  end;
end;

{procedura dodaj¹ca rekord z pliku (bazy danych)}
procedure dodaj_z_pliku (var head : wskaznik; x : book);
var
  e : wskaznik; // nowy element listy
  p : wskaznik; // wskaznik pomocniczy
begin
  New(e);
  e^.next := nil;
  e^.dane := x;
  p := head;
  if p = nil then
    head := e
  else
  begin
    while p^.next <> nil do // pêtla przesuwaj¹ca wskaznik na koniec listy
    begin
      p := p^.next;
    end;
    p^.next := e;
  end;
end;

{funkcja wyszukuj¹ca element listy na podtsawie podanych wartoœci}
function wyszukaj(head : wskaznik; x : string;
                 y : string; z : string; t : tdatetime) : wskaznik;
var
  p : wskaznik; // wskaznik pomocniczy
begin
  p := head;
  if p <> nil then
   begin
   try
   {pêtla sprawdzaj¹ca czy któryœ z elementów listy posiada
   IDENTYCZNE dane do tych podanych przez u¿ytkowanika}
     while (p^.dane.autor <> x) or
           (p^.dane.tytul <> y) or
           (p^.dane.wypo <> z) or
           (p^.dane.data <> t) do
             p := p^.next;
{funkcja zwraca wskaŸnik wskazuj¹cy na poszukiwany element listy}
     Result := p;
   except
     ShowMessage('Brak elementu na liœcie'); // w przypadku gdy nie znaleziono
   end;
   end
  else
   ShowMessage('Brak elementów na liscie.');  // gdy lista jest pusta
end;

{procedura usuwaj¹ca element z listy}
procedure usun(var head : wskaznik; e : wskaznik); // e - wskaznik na element usuwany
var
  p : wskaznik; // wskaznik pomocniczy
begin
  if head = e then  // je¿eli chcemy usun¹æ pierwszy element listy
  begin
    p := head;
    head := p^.next;
    dispose(p);
  end
  else
  begin
    p := head;
    while p^.next <> e do p := p^.next;  // pêtla poszukuj¹ca wskaznika e
    p^.next := e^.next;
    dispose(e);
  end;
end;

{procedura wypisuj¹ca listê na komponencie typu TLIstBox}
procedure odczyt(head : wskaznik; x : TListBox);
begin
x.Clear;  // oczyszczenie komponentu
  while head <> nil do
  begin
    x.Items.Add(head^.dane.autor);
    x.Items.Add(head^.dane.tytul);
    x.Items.Add(head^.dane.wypo);
    x.Items.Add(datetostr(head^.dane.data));
    x.Items.Add('');  // estetyczna przerwa miêdzy elementami listy
    head := head^.next; // przejœcie do nastêpnego elementu
  end;
end;

{procedura wypisuj¹ca dany element na komponencie typu TLIstBox}
procedure odczyt_pojedynczy(e : wskaznik; x : TListBox);
begin
 x.Items.Add(e^.dane.autor);
 x.Items.Add(e^.dane.tytul);
 x.Items.Add(e^.dane.wypo);
 x.Items.Add(datetostr(e^.dane.data));
 x.Items.Add('');
end;

{procedura wyszukuj¹ca i wypisuj¹ca wszystkie wypo¿yczone ksi¹¿ki danego autora}
procedure wyszukaj_autora (head : wskaznik; x : string;
                          y : TListBox);
var
  p : wskaznik;  // wskaŸnik pomocniczy
begin
  y.Clear;
  p := head;
  while p <> nil do
   begin
   try
     while (p^.dane.autor <> x) do  // pêtla szuka i wypisuje ksi¹¿ki danego autora
       begin
        p := p^.next;
        if p = nil then Break; // gdy natrafi na koniec listy
       end;
     if p <> nil then
       begin
        odczyt_pojedynczy(p, y); // odczyt jednej ksi¹¿ki
        p := p^.next;
       end;
   except
     ShowMessage('Brak elementu na liœcie');
   end;
  end
end;

{procedura wyszukuj¹ca i wypisuj¹ca wszystkie wypo¿yczone ksi¹¿ki
przez dan¹ osobê (to samo co procedura wy¿ej)}
procedure wyszukaj_wypozyczajacego (head : wskaznik; x : string;
                          y : TListBox);
var
  p : wskaznik;
begin
  y.Clear;
  p := head;
  while p <> nil do
   begin
   try
     while (p^.dane.wypo <> x) do
       begin
        p := p^.next;
        if p = nil then Break;
       end;
     if p <> nil then
       begin
        odczyt_pojedynczy(p, y);
        p := p^.next;
       end;
   except
     ShowMessage('Brak elementu na liœcie');
   end;
  end
end;

{Procedura modyfikuj¹ca element listy na podstawie podanych parametrów}
procedure zmien(x : string; y : string; z : string; t : TDateTime;
                 p : wskaznik);
begin
   p^.dane.autor := x;
   p^.dane.tytul := y;
   p^.dane.wypo := z;
   p^.dane.data := t;
end;

{procedura sortuj¹ca listê alfabetycznie tytu³ami}
procedure sortowanie_alfabetyczne(var head : wskaznik);
var
  p, e : wskaznik; // wskaŸniki pomocnicze
  i : book; // record pomocniczy
begin
  if head <> NIL then // sprawdzenie czy lista nie jest pusta
   begin
     p := head^.next;
     e := p;

     {sortowanie b¹belkowe}
     while (p <> NIL) do
      begin
       if (CompareText(head^.dane.tytul,p^.dane.tytul) > 0) then
        begin
         i := p^.dane;
         p^.dane:= head^.dane;
         head^.dane := i;
        end;
       p := p^.next;
      end;
      sortowanie_alfabetyczne(e);

   end
end;

{procedura filtruj¹ca i wyœwietlaj¹ca zawartoœæ listy na
podstaawie podanego przedzia³u czasu (nie zmieniaj¹c przy tym struktury listy)}
procedure filtruj_datami (head : wskaznik; listbox : TListBox;
                          x : TDateTime; y : TDateTime);
var
  p : wskaznik; // wskaŸnik pomocniczy
begin
  listbox.Clear;
  p := head;
  while p <> nil do
   begin
   {sprawdzenie czy ksi¹zka zosta³a wypo¿yczona
   w przedziale czasowym <x,y>}
     if (p^.dane.data >= x) and
        (p^.dane.data <= y) then
      odczyt_pojedynczy(p,listbox); // jeœli tak - wypisz
     p := p^.next; // przejdŸ do nastêpnego elementu
   end;
end;

{PRZYCISK CZYSZCZ¥CY WSZYSTKIE POLA}
procedure TTwypozyczalnia.TczyscClick(Sender: TObject);
begin
  Tautor_zapisz.Text := '';
  Ttytul_zapisz.Text := '';
  Twypo_zapisz.Text := '';
  Tdata_zapisz.Text := '';
  Tautor_zmien.Text := '';
  Ttytul_zmien.Text := '';
  Twypo_zmien.Text := '';
  Tdata_zmien.Text := '';
  Tautor_wyszukaj.Text := '';
  Twypo_wyszukaj.Text := '';
  Tod.Text := '';
  Tdo.Text := '';
end;

{PRZYCISK DODAJ}
procedure TTwypozyczalnia.TdodajClick(Sender: TObject);
begin
  dodaj(L,Tautor_zapisz.Text,Ttytul_zapisz.Text,
        Twypo_zapisz.Text,strtodate(Tdata_zapisz.Text));
end;

{PRZYCISK ODCZYT}
procedure TTwypozyczalnia.TodczytClick(Sender: TObject);
begin
  odczyt(L, Tlista);
end;

{PRZYCISK SKOPIUJ}
procedure TTwypozyczalnia.TskopiujClick(Sender: TObject);
begin
Tautor_zmien.Text := Tautor_zapisz.Text;
Ttytul_zmien.Text := Ttytul_zapisz.Text;
Twypo_zmien.Text := Twypo_zapisz.Text;
Tdata_zmien.Text := Tdata_zapisz.Text;
end;

{PRZYCISK SORTOWANIA}
procedure TTwypozyczalnia.TsortujClick(Sender: TObject);
begin
  sortowanie_alfabetyczne(L);
  odczyt(L, Tlista);
end;

{PRZYCISK USUÑ}
procedure TTwypozyczalnia.TusunClick(Sender: TObject);
begin
  usun(L, wyszukaj(L,Tautor_zapisz.Text,Ttytul_zapisz.Text,
        Twypo_zapisz.Text,strtodate(Tdata_zapisz.Text)));
end;

{PRZYCISK WCZYTAJ}
{odczytuje zawartoœæ pliku typowanego wstawiaj¹c j¹ w strukturê listy}
procedure TTwypozyczalnia.TwczytajClick(Sender: TObject);
var
  i : integer; // zmienna pomocnicza
  ksiazka : book; // rekord pomocniczy
begin
  if not FileExists(FileName) then Exit; // w przypadku gdy plik nie istnieje
  AssignFile(fp, FileName);

  {pêtla czyszcz¹ca listê}
  while L <> nil do
    begin
      usun(L,L)
    end;

  try
    Reset(fp);
    {odczytywanie kolejnych rekordów z pliku}
    for i := 0 to FileSize(fp) - 1 do
      begin
          read(fp,ksiazka);
          dodaj_z_pliku(L,ksiazka);
      end;
  finally
    CloseFile(fp);
  end;
end;

{PRZYCISK WYSZUKUJ¥CY OSOBÊ WYPO¯YCZAJ¥C¥}
procedure TTwypozyczalnia.Twyszukaj2Click(Sender: TObject);
begin
  wyszukaj_wypozyczajacego(L, Twypo_wyszukaj.Text, Tlista);
end;

{PRZYCISK WYSZUKUJ¥CY DATAMI}
procedure TTwypozyczalnia.Twyszukaj3Click(Sender: TObject);
begin
  filtruj_datami(L,Tlista,strtodate(Tod.Text),
                  strtodate(Tdo.Text));
end;

{PRZYCISK WYSZUKUJ¥CY AUTORA}
procedure TTwypozyczalnia.TwyszukajClick(Sender: TObject);
begin
  wyszukaj_autora(L, Tautor_wyszukaj.Text, Tlista);
end;

{PRZYCISK ZAPISUJ¥CY OBECN¥ LISTÊ DO PLIKU}
procedure TTwypozyczalnia.TzapiszClick(Sender: TObject);
var
  p : wskaznik; // wskaŸnik pomocniczy
  elem : book;   // rekord pomocniczy
begin
  AssignFile(fp, FileName);
  p := L;
  try
     rewrite(fp);

  {pêtla zapisuj¹ca po kolei elementy listy do pliku}
     while p <> nil do
       begin
         Write(fp, p^.dane);
         p := p^.next;
       end;

  finally
    CloseFile(fp);
  end;
end;

{PRZYCISK ZMIEÑ}
procedure TTwypozyczalnia.TzmienClick(Sender: TObject);
begin
  zmien(Tautor_zmien.Text,Ttytul_zmien.Text,
        Twypo_zmien.Text,strtodate(Tdata_zapisz.Text),
        wyszukaj(L,Tautor_zapisz.Text,Ttytul_zapisz.Text,
        Twypo_zapisz.Text,strtodate(Tdata_zapisz.Text)));
end;

begin
 L := nil;  // ustawienie wskaŸnika pocz¹tku listy na NIL (pusta lista - stan pocz¹tkowy)
end.


