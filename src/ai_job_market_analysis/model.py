from sklearn.linear_model import LinearRegression

def train_salary_model(df, target_col, feature_cols):
    model = LinearRegression()
    model.fit(df[feature_cols], df[target_col])
    return model
