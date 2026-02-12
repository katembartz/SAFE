from pathlib import Path
import numpy as np
import sys
import csv

def safe_for_slant(csv_fpath, code_dir):
    output_csv = str(csv_fpath).replace(".csv", "_slant_safe_results.csv")

    raw_data = np.genfromtxt(csv_fpath, delimiter=',', dtype=None, encoding='utf-8')

    labels = raw_data[0,:] 
    subjects = raw_data[1:,:] 

    def normalize_data(dataset):
        rows, cols = dataset.shape
        norm_data = np.empty((rows,cols-2),dtype=object)
        brain_vol = np.zeros((rows,1))

        for i in range(rows):
            temp = 0
            for j in range(cols-2):
                j += 2
                temp += float(dataset[i,j])
            brain_vol[i,0] = temp

        for i in range(rows):
            for j in range(cols-2):
                j += 2
                if brain_vol[i,0] == 0:
                    norm_data[i,j-2] = 0
                else:
                    norm_data[i,j-2] = str(float(dataset[i,j])/brain_vol[i,0]*100)
        return norm_data

    r_rows, r_cols = raw_data.shape
    NV_labels = np.empty((r_cols-6), dtype=object) 
    NV_labels[0:2] = labels[0:2] 
    NV_labels[2:17] = labels[4:19] 
    NV_labels[17:] = labels[23:] 
    NV_subjects = np.empty((r_rows-1,r_cols-6), dtype=object)
    NV_subjects[:,0:2] = subjects[:,0:2]
    NV_subjects[:,2:17] = subjects[:,4:19]
    NV_subjects[:,17:] = subjects[:,23:]

    NV_norm_data = normalize_data(NV_subjects)
    NV_rows, NV_cols = NV_norm_data.shape

    vol_data = np.empty((NV_rows+1,NV_cols+1), dtype=object)
    vol_data[:,0] = raw_data[:,0]
    vol_data[0,1:] = NV_labels[2:]
    vol_data[1:,1:] = NV_subjects[:,2:] 

    NV_mod_data = np.empty((NV_rows+1,NV_cols+1), dtype=object)
    NV_mod_data[0,1:] = NV_labels[2:] 
    NV_mod_data[:,0] = raw_data[:,0] 
    NV_mod_data[1:,1:] = NV_norm_data 

    mu_std_norm = np.genfromtxt(code_dir/"NV_occup_slant_norm_vol.csv", delimiter=',', dtype=None, encoding='utf-8')
    mu_std_vol = np.genfromtxt(code_dir/"NV_slant_norm_vol.csv", delimiter=',', dtype=None, encoding='utf-8')

    def summarize_stats(mu_std_norm, mu_std_vol, data_norm, data_vol):
        rows, cols = data_norm.shape
        occ_95 = np.empty(rows-1, dtype=object) 
        occ_95[:] = [[] for _ in range(rows - 1)] 
        occ_99 = np.empty(rows-1, dtype=object) 
        occ_99[:] = [[] for _ in range(rows - 1)]
        zeros = np.empty(rows-1, dtype=object) 
        zeros[:] = [[] for _ in range(rows - 1)]
        vol_95 = np.empty(rows-1, dtype=object) 
        vol_95[:] = [[] for _ in range(rows - 1)]
        vol_99 = np.empty(rows-1, dtype=object) 
        vol_99[:] = [[] for _ in range(rows - 1)]

        for i in range(rows-1):
            i = i + 1
            for j in range(cols-1):
                j = j + 1
                label = data_norm[0,j]
                curr_norm = float(data_norm[i,j])
                curr_vol = float(data_vol[i,j])

                if curr_norm == 0:
                    zeros[i-1].append(label)

                mu_norm = float(mu_std_norm[j,1])
                std_norm = float(mu_std_norm[j,2])
                offset = round((curr_norm - mu_norm)/std_norm,6) # determine offset

                mu_vol = float(mu_std_vol[j,1])
                std_vol = float(mu_std_vol[j,2])
                vol_offset = round((curr_vol - mu_vol)/std_vol,6)

                if abs(offset) >= 3:
                    occ_99[i-1].append(label)
                elif abs(offset) >= 2:
                    occ_95[i-1].append(label)

                if abs(vol_offset) >= 3:
                    vol_99[i-1].append(label)
                elif abs(vol_offset) >= 2:
                    vol_95[i-1].append(label)

        return occ_95, occ_99, zeros, vol_95, vol_99

    occ_95, occ_99, zeros, vol_95, vol_99 = summarize_stats(mu_std_norm, mu_std_vol, NV_mod_data, vol_data) # get summary data
    rows, cols = NV_mod_data.shape

    with open(output_csv, 'w') as f:
        f.write('subject,')
        f.write('decision,')
        f.write('zero_count,')
        f.write('occ_95_count,')
        f.write('occ_99_count,')
        f.write('vol_95_count,')
        f.write('vol_99_count,')
        f.write('zero_regions,')
        f.write('occ_95_regions,')
        f.write('occ_99_regions,')
        f.write('vol_95_regions,')
        f.write('vol_99_regions')
        f.write("\n")
        
        writer = csv.writer(f)
        
        for i in range(rows-1):
            subj = NV_mod_data[i+1,0]
            f.write(f'{subj},')
            
            curr_zeros = len(zeros[i],)
            curr_occ_95 = len(occ_95[i],)
            curr_occ_99 = len(occ_99[i],)
            curr_vol_95 = len(vol_95[i],)
            curr_vol_99 = len(vol_99[i],)

            if curr_occ_99 > 5 or curr_zeros > 0 or curr_vol_99 > 5:
                f.write('reject,')
            else:
                f.write('accept,')
                
            f.write(f'{curr_zeros},')
            f.write(f'{curr_occ_95},')
            f.write(f'{curr_occ_99},')
            f.write(f'{curr_vol_95},')
            f.write(f'{curr_vol_99},')
                
            writer.writerow([
                ",".join(zeros[i]),
                ",".join(occ_95[i]),
                ",".join(occ_99[i]),
                ",".join(vol_95[i]),
                ",".join(vol_99[i])
            ])
        
    print(f"Safe decisions for slant saved in {output_csv}")