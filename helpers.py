from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import mean_squared_error, r2_score
import prettytable
import pandas as pd


def compute_test_train_error(model, X, y):
    
  t = prettytable.PrettyTable()
  t.field_names = ["J_train", "J_test", "R2_test"]

  for s in t.field_names:
    t.align[s] = "l"
    t.float_format[s] = "0.8"
    
  n_splits = 3
  rs = ShuffleSplit(n_splits=n_splits, test_size=0.3, random_state=42)
  
  j_train, j_test, r2_test = [], [], []
  
  if isinstance(X, pd.DataFrame):
    indexer = lambda d, idx: d.loc[idx,:]
  else:
    indexer = lambda x, idx: x[idx,:]
  
  for i, (train_index, test_index) in enumerate(rs.split(y)):
    print("Training split %d of %d" % (i + 1, n_splits))

    X_train, X_test, y_train, y_test = \
      indexer(X, train_index), \
      indexer(X, test_index), \
      y[train_index], \
      y[test_index]

    model.fit(X_train, y_train)

    y_pred_test = model.predict(X_test)
    j_train.append(mean_squared_error(y_train, model.predict(X_train)))    
    j_test.append(mean_squared_error(y_test, y_pred_test))
    r2_test.append(r2_score(y_test, y_pred_test))

    t.add_row([j_train[-1], j_test[-1], r2_test[-1]])

  t.add_row([sum(j) /n_splits for j in (j_train, j_test, r2_test)])
  print(t)
