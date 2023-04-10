class DeepLearningDataConverter:
    # Converts dataframe columns specified into the original column (positive)
    # and a new column to represent if its negative
    @staticmethod
    def add_positive_columns(df, columns):
        for column in columns:
            df[column + "_positive"] = df[column]
            df[column + "_is_negative"] = df[column].apply(lambda x: 1 if x == 0 else 0)
            df.drop(column, axis=1, inplace=True)
        return df
