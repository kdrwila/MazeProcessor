#!/usr/bin/perl
# Karol Drwila gr1

# eval "use Switch; 1" or die "Błąd! Nie znaleziono modułu `Switch`, program zostanie zamknięty.";

# use Switch;

# require Switch or die "you need Module to run this program";
# Switch->import;

my $rc = eval
{
	require Switch;
	1;
};

if(!$rc)
{
	print "Błąd! Nie znaleziono modułu `Switch`, program zostanie zamknięty.\n";
	exit 1;
}

use Switch;

foreach(@ARGV)
{
    if($_ eq "-h")
    {
        print "========================================\n";
        print "Skrypt walk_maze.pl, autor: Karol Drwiła\n";
        print "Skrypt na podstawie otrzymanych danych szuka najkrótszej scieżki w labiryncie przy użyciu algorytmu DFS, a każdą zmianę stanu elementu labiryntu wypisuje wypisuje na stdout.\n";
        print "Skrypt używa biblioteki Switch\n\n";
        print "Skrypt nie został stworzony z myślą o samodzielnym używaniu, a jedynie jako część większego skryptu, więc nie podaje informacji co jest nie tak z danymi, które otrzymał.\n\n";
        print "Przyjmowane rgumenty:\n\n";
        print "-h - skrypt wypisuje pomoc dla skryptu.\n\n";
        print "sprepraowany ciąg znaków w formacie \"x,y|xn,yn/xn,yn/...;x,y|xn,yn/xn,yn/...;...\" - skrypt intepretuje przesłane dane i na ich podstawie wykonuje operacje opisane wyżej w jego opisie.\n\n";
        print "========================================\n";

        exit 0;
    }
}

if(scalar @ARGV == 0)
{
    print "Nie podano żadnych argumentów, program zostanie zakończony\n";
    exit 1;
}

my @matrix;

my @cells = split /;/, $ARGV[0];

my $max_x;
my $max_y;

foreach(@cells)
{
    @cell_data = split /\|/, $_;
    if(scalar @cell_data != 2)
    {
        print "Błąd poprawności danych, program zostanie zakończony\n";
        exit 1;
    }

    @coords = split /,/, $cell_data[0];

    if(scalar @coords != 2)
    {
        print "Błąd poprawności danych, program zostanie zakończony\n";
        exit 1;
    }

    $matrix[$coords[0]][$coords[1]] = $cell_data[1];

    $max_x = $coords[0];
    $max_y = $coords[0];
}

my @coords = split /:/, $ARGV[1];

if($coords[0] > $max_x || $coords[1] > $max_x || $coords[0] < 0 || $coords[1] < 0)
{
    print "Błąd poprawności danych, program zostanie zakończony\n";
    exit 1;
}

my $start_x = $coords[0];
my $start_y = $coords[1];

my @coords = split /:/, $ARGV[2];

if($coords[0] > $max_x || $coords[1] > $max_x || $coords[0] < 0 || $coords[1] < 0)
{
    print "Błąd poprawności danych, program zostanie zakończony\n";
    exit 1;
}

my $end_x = $coords[0];
my $end_y = $coords[1];

my @queue;
my @visited;
my @direction;

push @queue, $start_x;
push @queue, $start_y;

push @visited, "$start_x,$start_y";

while(scalar @queue > 1)
{
    my $w = shift @queue;
    my $k = shift @queue;

    print "v$w:$k|\n";

    if($w == $end_x && $k == $end_y)
    {
        last;
    }

    my @neighbors = split /\//, $matrix[$w][$k];

    foreach(@neighbors)
    {
        @coords = split /,/, $_;

        if(!($_ ~~ @visited))
        { 
            push @queue, $coords[0];
            push @queue, $coords[1];

            if($coords[0] > $w && $coords[1] == $k) 
            {
                $direction[$coords[0]][$coords[1]] = 'l';
            }
            if($coords[0] < $w && $coords[1] == $k)
            {
                $direction[$coords[0]][$coords[1]] = 'r';
            }
            if($coords[0] == $w && $coords[1] < $k)
            {
                $direction[$coords[0]][$coords[1]] = 'u';
            }
            if($coords[0] == $w && $coords[1] > $k) 
            {
                $direction[$coords[0]][$coords[1]] = 'd';
            }

            push @visited, $_;
        }
    }
}

$w = $end_x;
$k = $end_y;

while($w != $start_x || $k != $start_y)
{
    print "p$w:$k|\n";

    switch($direction[$w][$k])
    {
        case 'd' 
        {
            $k--;
        }
        case 'u' 
        {
            $k++;
        }
        case 'r' 
        {
            $w++;
        }
        case 'l' 
        {
            $w--;
        }
    }
}

print "p$start_x:$start_y|\n";

foreach(@visited)
{
    @coords = split /,/, $_;

    print "a$coords[0]:$coords[1]|\n";
}

exit 0;