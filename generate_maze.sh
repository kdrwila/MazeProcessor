#!/bin/bash
# Karol Drwila gr1

for var in "$@"
do
	case "$var" in
        "-h")
            echo "====================================="
            echo "generate_maze.sh, autor: Karol Drwila"
            echo
            echo "Skrypt generuje labirynt metoda Wilsona. Skrypt jest czescia skryptu generateMaze.py i nie powinien byc uruchamiany samodzielnie, ze wzgledu na znikome sprawdzanie poprawnosci danych."
            echo
            echo "Uruchamianie:"
            echo
            echo "bash generate_maze.sh i_w i_k [-h] np."
            echo "bash generate_maze.sh 3 3"
            echo 
            echo " i_k - liczba, ilosc kolumn labiryntu"
            echo " i_w - liczba, ilosc wierszy labiryntu"
            echo " -h  - uruchamia pomoc dotyczaca skryptu"
            echo "====================================="
            exit 1
        ;;
    esac
done

NEIGHBOR_LEFT=1
NEIGHBOR_TOP=2
NEIGHBOR_RIGHT=4
NEIGHBOR_BOTTOM=8

found_added=0
first_x=-1
first_y=-1

re='^[0-9]+$'
if ! [[ $1 =~ $re ]]
then
   echo "Blad, pierwszy argument nie jest liczba calkowita" >&2
   exit 1
fi

re='^[0-9]+$'
if ! [[ $2 =~ $re ]]
then
   echo "Blad, drugi argument nie jest liczba calkowita" >&2
   exit 1
fi

count_x=$1
count_y=$2


element_count=$[$1 * $2]
elements=()

matrix_write () 
{
    eval $1"_"$2"_"$3=$4
}

matrix_read () 
{
    aux=$1"_"$2"_"$3
    matrix_read_ret=${!aux}
}

random_max ()
{
    local buf=$[$RANDOM % $1]
    random_max_ret=$buf
}

getRandomElement ()
{
    len=${#elements[@]}
    random_max $len
    rand=$random_max_ret

    get_random_element_ret=${elements[$rand]}
}

getXYFromString ()
{
    IFS=':' read -ra ADDR <<< "$1"
    count=0
    for i in "${ADDR[@]}"; do
        if (( count == 0 ))
        then
            get_xy_from_string_ret_x=$i
        fi
        if (( count == 1 ))
        then
            get_xy_from_string_ret_y=$i
        fi
        count=$[$count + 1]
    done
}

sendOneCellDataToOutput ()
{
    matrix_read cell_added $1 $2
    added=$matrix_read_ret
    matrix_read cell_current $1 $2
    current=$matrix_read_ret
    matrix_read cell_visiting $1 $2
    visiting=$matrix_read_ret
    matrix_read cell_neighbors $1 $2
    neighbors=$matrix_read_ret
    printf "d%d,%d,%d,%d,%d,%d|\n" "$1" "$2" "$added" "$current" "$visiting" "$neighbors"
}

resetWalkData ()
{
    for (( x=0; x<$count_x; x++ ))
    do
        for (( y=0; y<$count_y; y++ ))
        do
            matrix_read cell_visiting $x $y
            if (( $matrix_read_ret != 0 ))
            then
                matrix_write cell_visiting $x $y 0
                matrix_write cell_current $x $y 0
                matrix_write cell_direction $x $y -1
                sendOneCellDataToOutput $x $y
            fi
        done
    done
}

addNeighbor ()
{
    matrix_read cell_neighbors $1 $2
    temp=$(($matrix_read_ret|$3))
    matrix_write cell_neighbors $1 $2 $temp
}

createMazePath ()
{
    matrix_read cell_added $first_x $first_y
    cmp_added=$matrix_read_ret
    while (( cmp_added != 1 ))
    do
        before_x=$first_x
        before_y=$first_y
        
        matrix_read cell_direction $first_x $first_y
        case $matrix_read_ret in
            0) # left
                addNeighbor $first_x $first_y $NEIGHBOR_LEFT
                first_x=$[$first_x - 1]
                addNeighbor $first_x $first_y $NEIGHBOR_RIGHT
            ;;
            1) # up
                addNeighbor $first_x $first_y $NEIGHBOR_TOP
                first_y=$[$first_y - 1]
                addNeighbor $first_x $first_y $NEIGHBOR_BOTTOM
            ;;
            2) # right
                addNeighbor $first_x $first_y $NEIGHBOR_RIGHT
                first_x=$[$first_x + 1]
                addNeighbor $first_x $first_y $NEIGHBOR_LEFT
            ;;
            3) # down
                addNeighbor $first_x $first_y $NEIGHBOR_BOTTOM
                first_y=$[$first_y + 1]
                addNeighbor $first_x $first_y $NEIGHBOR_TOP
            ;;
        esac

        matrix_read cell_added $first_x $first_y
        cmp_added=$matrix_read_ret
        sendOneCellDataToOutput $first_x $first_y
        removeElementFromList $before_x $before_y
        sendOneCellDataToOutput $before_x $before_y
    done

    resetWalkData
}

createMaze ()
{
    found_added=0
    getRandomElement
    getXYFromString $get_random_element_ret 
    rand_x=$get_xy_from_string_ret_x
    rand_y=$get_xy_from_string_ret_y
    rand_x=$[$rand_x]
    rand_y=$[$rand_y]

    matrix_write cell_current $rand_x $rand_y 1
    matrix_write cell_visiting $rand_x $rand_y 1

    first_x=$rand_x
    first_y=$rand_y

    while (( found_added < 1 ))
    do
        next_x=$rand_x
        next_y=$rand_y
        random_max 4
        direction=$random_max_ret
        case $direction in
            0) # left
                if (( rand_x != 0 ))
                then
                    next_x=$[$rand_x - 1]
                    next_y=$rand_y
                fi
            ;;
            1) # up
                if (( rand_y != 0 ))
                then
                    next_x=$rand_x
                    next_y=$[$rand_y - 1]
                fi
            ;;
            2) # right
                if (( rand_x != $[$count_x - 1] ))
                then
                    next_x=$[$rand_x + 1]
                    next_y=$rand_y
                fi
            ;;
            3) # down
                if (( rand_y != $[$count_y - 1] ))
                then
                    next_x=$rand_x
                    next_y=$[$rand_y + 1]
                fi
            ;;
        esac

        matrix_read cell_added $next_x $next_y
        if (( matrix_read_ret == 1 ))
        then
            found_added=1
            matrix_write cell_direction $rand_x $rand_y $direction
            createMazePath
        else
            matrix_write cell_current $rand_x $rand_y 0
            sendOneCellDataToOutput $rand_x $rand_y

            matrix_write cell_visiting $next_x $next_y 1
            matrix_write cell_current $next_x $next_y 1
            sendOneCellDataToOutput $next_x $next_y

            matrix_write cell_direction $rand_x $rand_y $direction
        fi

        rand_x=$next_x
        rand_y=$next_y

    done
}

removeElementFromList ()
{
    matrix_write cell_added $1 $2 1
    matrix_write cell_visiting $1 $2 0
    matrix_write cell_current $1 $2 0
    matrix_write cell_direction $1 $2 -1
    element_count=$[$element_count - 1]

    index=0
    for i in "${!elements[@]}"; do
        if [[ "${elements[$i]}" = "$1:$2" ]]; then
            index=$i;
        fi
    done

    unset elements[$index]
    elements=("${elements[@]}")
}

for (( x=0; x<$1; x++ ))
do
    for (( y=0; y<$2; y++ ))
    do
        matrix_write cell_visiting $x $y 0
        matrix_write cell_current $x $y 0
        matrix_write cell_added $x $y 0
        matrix_write cell_direction $x $y -1
        matrix_write cell_neighbors $x $y 0
        elements+=("$x:$y")
    done
done

random_max $1
rand_x=$random_max_ret
random_max $2
rand_y=$random_max_ret

removeElementFromList $rand_x $rand_y
sendOneCellDataToOutput $rand_x $rand_y

while (( $element_count > 0 ))
do
    createMaze
done

exit 0