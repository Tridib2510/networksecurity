import os
import sys
import mlflow
import dagshub
dagshub.init(repo_owner='tridibroychowdhury9', repo_name='networksecurity', mlflow=True)
# whenever we use mlflow it will automatically log in dagshub
# Dagshub is a platform that combines version control, data management, and collaboration tools for
#  machine learning projects. It integrates with Git and GitHub to 
# provide a seamless workflow for data scientists and machine learning engineers.
from networksecurity.exception.exception import NetworkSecurtiyException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object,evaluate_models
from networksecurity.utils.main_utils.utils import load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification_metric import get_classifcation_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
    
)

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurtiyException(e,sys)
    def track_mlflow(self,best_model,classificationmetric):
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score

            mlflow.log_metric("f1_socre",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")

    
    def train_model(self,X_train,y_train,x_test,y_test):
        models={
            "Random Forest":RandomForestClassifier(verbose=1),
            # verbose=1 → Shows minimal information about training progress.
            # Higher values (e.g., verbose=2, 3…) → More detailed logging.
            "Decision Tree":DecisionTreeClassifier(),
            "Gradient Boosting":GradientBoostingClassifier(),
            "AdaBoost":AdaBoostClassifier(),
        }
        # Performing hyperparameter tuning
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }

            
        }
        model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=x_test,y_test=y_test,models=models,param=params)
        
        # To get the best model score from the dict
        best_model_score=max(sorted(model_report.values()))

        # To get the best model name from the dict
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]


        best_model=models[best_model_name]
        y_train_pred=best_model.predict(X_train)

        classification_train_metric=get_classifcation_score(y_true=y_train,y_pred=y_train_pred)
        
        # Will write a function to track the mf flow later
        # mf flow is open source tool that would help to maintain the entire lifeqycle of the model
        # of our datascience project

        # Track the experiments with mlflow
        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred=best_model.predict(x_test)
        classsification_test_metric=get_classifcation_score(y_true=y_test,y_pred=y_test_pred)

        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        # The Network model can be directly used to perform prediction on new data
        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)
        
        # We need to push the model.pkl and preprocessor.pkl file and push it to 
        # one commmon folder from where we are going to do prediction

        
        # Here we save the model in a file named model.pkl inside a folder named final_model
        save_object("final_model/model.pkl",best_model)

        # Model Trainer  Artifact
        model_trainer_artifact= ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classsification_test_metric
                             )
        logging.info(f"Model trainer artifact:{model_trainer_artifact}")

        return model_trainer_artifact

    def initiate_model_trainer(self)->ModelTrainerArtifact:
       try:
        #    train_file_path=self.data_transformation_artifact.transformed_train_file_path
           train_file_path=self.data_transformation_artifact.transformed_train_file_path
           test_file_path=self.data_transformation_artifact.transformed_test_file_path


        #    Loading trainig array and testing array
           train_arr=load_numpy_array_data(train_file_path)
           test_arr=load_numpy_array_data(test_file_path)

           x_train,y_train,x_test,y_test=(
               train_arr[:,:-1],
               train_arr[:,-1],#just taking the last column
               test_arr[:,:-1],
               test_arr[:,-1]
           )

           model=self.train_model(x_train,y_train,x_test,y_test)
           
       except Exception as e:
           raise NetworkSecurtiyException(e,sys)
        
