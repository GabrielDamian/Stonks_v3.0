import csv

def readDataFromFile(fileName,linesToRead):
    print("Citesc date din fisier...")
    vector = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                pass

                y = row[1].split()

                if len(y) >= 2:
                    z = y[1].split(':')
                    final_time = int(z[1])

                vector.append(row[3])
                line_count += 1
            linesToRead -= 1
            if linesToRead< 0:
                break
        # print(f'Processed {line_count} lines.')

        #primul elem din arr este un header de tip string (trash de la citire)
        del vector[0]
        #inverseaza ordinea in vector
        # vector = vector[::-1]

        float_arr = []
        for x in vector:
            float_arr.append(float(x))
        return float_arr
def yEcuatieDreapta(point_a, point_b, x_value):
    x0 = point_a[0]
    y0 = point_a[1]

    x1 = point_b[0]
    y1 = point_b[1]

    x = x_value

    y = (y0*(x1-x) + y1*(x-x0))/(x1-x0)

    return y

def interpolare_segmente(segment_referinta, segment_factorizat):
    #cauta indicii x din segmentul referinta printre indicii (la propriu intre care se situeaza) in segmentul factorizat

    segment_rezultat = []
    x_segment_referinta = [a[0] for a in segment_referinta]
    x_segment_factorizat = [a[0] for a in segment_factorizat]

    # print('x_segment_referinta:', x_segment_referinta)
    # print('x_segment_factorizat:',x_segment_factorizat)

    for a in x_segment_referinta:
        x_current = a

        if x_current in x_segment_factorizat:
            #avem punct comun intre cele segmente
            x_y_factorizat_aferent = None
            for temp in segment_factorizat:
                if x_current == temp[0]:
                    x_y_factorizat_aferent = temp
                    break
            pereche_noua = [x_current, x_y_factorizat_aferent[1]]

            segment_rezultat.append(pereche_noua)

        else:
            #gaseste indicii intre care se situeaza
            prev_index =segment_factorizat[0]
            next_index = None
            index = 1
            while index < len(segment_factorizat):
                next_index = segment_factorizat[index]
                if prev_index[0] < x_current and x_current < next_index[0]:
                    pereche_noua =[x_current, round(yEcuatieDreapta(prev_index, next_index, x_current),2)]
                    segment_rezultat.append(pereche_noua)
                    break
                else:
                    index +=1
                    prev_index = next_index


    # print('Interpolare_final:', segment_rezultat)

    #adauga ultimul index manual

    if len(segment_rezultat) < len(segment_referinta):
        segment_rezultat.append([segment_referinta[-1][0], segment_factorizat[-1][1]])
    return segment_rezultat




def comprimaInterpoleazaSegment(segment_mic, segment_mare):
    #+ factorizeaza segment
    size_mic = len(segment_mic)
    size_mare = len(segment_mare)

    #[a, a, a, a, a]
    #[1, 5, 7, 9, 7, 4, 2]

    x_mic = []
    y_mic = []
    for a in segment_mic:
        x_mic.append(a[0])
        y_mic.append(a[1])

    max_height_seg_mic = max(y_mic)
    max_width_seg_mic = max(x_mic)


    x_mare = []
    y_mare = []
    for a in segment_mare:
        x_mare.append(a[0])
        y_mare.append(a[1])

    max_height_seg_mare = max(y_mare)
    max_width_seg_mare = max(x_mare)

    factor_height = round(max_height_seg_mic / max_height_seg_mare,2)
    factor_width = round(max_width_seg_mic / max_width_seg_mare,2)
    #factorizare inaltime din segment mare catre segment mic (fie ea subunitara sau supraunitara)

    y_mare_factorizat = [a*factor_height for a in y_mare]

    #factorizare width

    x_mare_facotirizat = [a*factor_width for a in x_mare]

    segment_mare_factorizat = []
    for index, a in enumerate(y_mare_factorizat):
        segment_mare_factorizat.append([x_mare_facotirizat[index],a])

    final_fact_interpolat = interpolare_segmente(segment_mic, segment_mare_factorizat)

    return final_fact_interpolat
