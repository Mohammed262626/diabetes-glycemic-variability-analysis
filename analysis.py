import pandas as pd
import glob
import os
import sys
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def run_advanced_medical_analysis():
    # 1. Batch Import Setup
    data_folder = "./"  
    file_pattern = os.path.join(data_folder, "data-*")
    all_files = sorted(glob.glob(file_pattern))
    
    if not all_files:
        print("Error: No patient data files found.")
        return

    patient_dfs = []
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        patient_id = file_name.split("-")[1]
        try:
            single_df = pd.read_csv(
                file_path, sep='\t', 
                names=['date', 'time', 'code', 'value'],
                header=None, dtype={'code': int, 'value': str}
            )
            single_df['patient_id'] = f"Patient_{patient_id}"
            patient_dfs.append(single_df)
        except Exception:
            continue

    master_df = pd.concat(patient_dfs, ignore_index=True)
    master_df['value'] = pd.to_numeric(master_df['value'], errors='coerce')
    master_df = master_df.dropna(subset=['value'])

    # 2. Map Glucose Readings
    glucose_codes = {
        57: 'Pre-breakfast',
        58: 'Post-breakfast',
        59: 'Pre-lunch',
        60: 'Post-lunch',
        61: 'Pre-dinner',
        62: 'Post-dinner',
        64: 'Post-bedtime'
    }
    glucose_df = master_df[master_df['code'].isin(glucose_codes.keys())].copy()
    glucose_df['time_of_day'] = glucose_df['code'].map(glucose_codes)

    # 3. Setup Advanced Reporting Output
    output_report_path = "advanced_clinical_analysis.txt"
    with open(output_report_path, 'w') as f:
        sys.stdout = f
        
        print("==============================================================================")
        print("                ADVANCED BIOSTATISTICAL ANALYSIS REPORT                      ")
        print("==============================================================================")
        print(f"Total Cohort Size : {master_df['patient_id'].nunique()} Patients")
        print(f"Total Observations: {glucose_df.shape[0]} Cleaned Glucose Records")
        print("==============================================================================\n")
        
        # --- TEST 1: ONE-WAY ANOVA ---
        print("TEST 1: GLOBAL VARIANCE ASSESSMENT (ONE-WAY ANOVA)")
        print("-" * 78)
        groups = [group['value'].values for name, group in glucose_df.groupby('time_of_day') if len(group) > 1]
        f_stat, anova_p = stats.f_oneway(*groups)
        print(f"F-Statistic: {f_stat:.4f}")
        print(f"p-Value    : {anova_p:.4e}")
        print(f"Significance: {'Significant (p<0.05)' if anova_p < 0.05 else 'Not Significant'}\n")

        # --- TEST 2: TUKEY HSD POST-HOC COMPASS ---
        print("TEST 2: PAIRWISE DIFFERENCE MATRIX (TUKEY HSD POST-HOC)")
        print("-" * 78)
        if anova_p < 0.05:
            tukey = pairwise_tukeyhsd(endog=glucose_df['value'],
                                      groups=glucose_df['time_of_day'],
                                      alpha=0.05)
            # Convert Tukey summary table to string for neat file printing
            print(tukey.summary().as_text())
        else:
            print("Skipped: Post-Hoc comparisons are not executed if global ANOVA is non-significant.")
        print("\n" + "=" * 78 + "\n")

        # --- TEST 3: PAIRED T-TEST (PRE VS POST BREAKFAST PHYSIOLOGICAL CHANGEOVER) ---
        print("TEST 3: DEPENDENT SAMPLES ASSESSMENT (PAIRED T-TEST)")
        print("-" * 78)
        print("Objective: Evaluate physiological glucose shift from Pre-Breakfast to Post-Breakfast")
        print("           within individual patients on the exact same recording dates.")
        
        # Extract paired records
        pre_b = glucose_df[glucose_df['time_of_day'] == 'Pre-breakfast'][['patient_id', 'date', 'value']].rename(columns={'value': 'pre_val'})
        post_b = glucose_df[glucose_df['time_of_day'] == 'Post-breakfast'][['patient_id', 'date', 'value']].rename(columns={'value': 'post_val'})
        
        # Merge on Patient ID and Date to create perfectly matched rows
        paired_df = pd.merge(pre_b, post_b, on=['patient_id', 'date']).dropna()
        
        print(f"Total matched paired dates isolated across cohort: {paired_df.shape[0]}")
        
        if paired_df.shape[0] >= 5:
            t_stat, paired_p = stats.ttest_rel(paired_df['pre_val'], paired_df['post_val'])
            mean_diff = (paired_df['post_val'] - paired_df['pre_val']).mean()
            
            print(f"Mean Glycemic Shift  : {mean_diff:+.2f} mg/dL")
            print(f"Calculated t-Value   : {t_stat:.4f}")
            print(f"Two-Tailed p-Value   : {paired_p:.4e}")
            print(f"Interpretation       : {'Statistically Significant (p<0.05)' if paired_p < 0.05 else 'No significant mean difference observed.'}")
            if paired_p < 0.05:
                print("Conclusion           : Reject the null hypothesis. Post-prandial metabolization")
                print("                       causes a distinct, quantifiable shift in glycemic tracking.")
        else:
            print("Insufficient paired longitudinal metrics available for dependent t-test execution.")
        print("==============================================================================")

    sys.stdout = sys.__stdout__
    print(f"Success! Advanced analysis compiled and exported to: {output_report_path}")

if __name__ == "__main__":
    run_advanced_medical_analysis()