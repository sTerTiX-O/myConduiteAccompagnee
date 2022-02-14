# -*- coding: utf-8 -*-

from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
import sqlite3
from sqlite3 import Error
import uuid



app = Flask(__name__)



#
#
# API (Flask)
#
#


@app.route("/createDrivingSession", methods=['GET'])
def createDrivingSession():
    uuidDrivingSession = MCADrivingSessionService_createDrivingSession() 
    return str(uuidDrivingSession)


@app.route("/deleteDrivingSession/<uuidDeletedDrivingSession>", methods=['GET'])
def deleteDrivingSession(uuidDeletedDrivingSession):
    MCADrivingSessionService_deleteDrivingSession(uuidDeletedDrivingSession)
    return uuidDeletedDrivingSession


@app.route("/updateDrivingSessionsInfos/<uuidModifiedDrivngSessions>/newname/<newDrivingSessionName>")
def updateDrivingSessionsInfos(uuidModifiedDrivngSessions, newDrivingSessionName):
    MCADrivingSessionService_updateDrivingSessionsInfos(uuidModifiedDrivngSessions, newDrivingSessionName)
    return newDrivingSessionName


@app.route("/fetchDrivingSessionsInfos/<uuidDrivingSessionInfoWantedToBeFetch>")
def fetchDrivingSessionsInfos(uuidDrivingSessionInfoWantedToBeFetch):
    MCADrivingSessionService_fetchDrivingSessionsInfos(uuidDrivingSessionInfoWantedToBeFetch)
    return uuidDrivingSessionInfoWantedToBeFetch


@app.route("/fetchAllDrivingSessions")
def fetchAllDrivingSessions():
    AllDrivingSessions = MCADrivingSessionService_fetchAllDrivingSessions()
    return jsonify(AllDrivingSessions)






#
#
# Service (MCADrivingSessionService)
#
#

def MCADrivingSessionService_createDrivingSession():
    uuidDrivingSession = uuid.uuid4()
    drivingSession = (str(uuidDrivingSession), 'Session Matinale', '2023/12/26Z13:37:37', '2023/12/26Z13:57:45')
    print("Creation session conduite uuidDrivingSession=[{}]".format(uuidDrivingSession))
    MCADataBaseAccess_insertDrivingSession(drivingSession)
    return uuidDrivingSession


def MCADrivingSessionService_deleteDrivingSession(uuidDeletedDrivingSession):
    MCADataBaseAccess_deleteDrivingSession(uuidDeletedDrivingSession)
    print("Destruction session conduite uuidDeletedDrivingSession=[{}]".format(uuidDeletedDrivingSession))
    return uuidDeletedDrivingSession


def MCADrivingSessionService_updateDrivingSessionsInfos(uuidModifiedDrivngSessions, newDrivingSessionName):
    MCADataBaseAccess_updateDrivingSessionsInfos(uuidModifiedDrivngSessions, newDrivingSessionName)
    print("Modification infos avec uuidModifiedDrivngSessions=[{}] et newname=[{}]".format(uuidModifiedDrivngSessions, newDrivingSessionName))
    return uuidModifiedDrivngSessions, newDrivingSessionName


def MCADrivingSessionService_fetchDrivingSessionsInfos(uuidDrivingSessionInfoWantedToBeFetch):
    print("Récuperation des données avec uuidDrivingSessionInfoWantedToBeFetch=[{}] ...".format(uuidDrivingSessionInfoWantedToBeFetch))
    MCADataBaseAccess_fetchDrivingSessionsInfos(uuidDrivingSessionInfoWantedToBeFetch)


def MCADrivingSessionService_fetchAllDrivingSessions():
    print("Récuperation des driving sessions ...")
    gigi = MCADataBaseAccess_fetchAllDrivingSessions()
    return gigi






#
#
# Database access (MCADataBaseAccess)
#
#

def MCADataBaseAccess_insertDrivingSession(drivingSession):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    # create a database connection
    conn = MCADataBaseAccess_create_connection()
    with conn:
        sqlRequest = ''' INSERT INTO drivingsessions(id,name,begin_date,end_date)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sqlRequest, drivingSession)
        conn.commit()
        return cur.lastrowid


def MCADataBaseAccess_deleteDrivingSession(uuidDeletedDrivingSession, ):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    conn = MCADataBaseAccess_create_connection()
    with conn:
        sql = 'DELETE FROM drivingsessions WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (uuidDeletedDrivingSession,))
        conn.commit()


def MCADataBaseAccess_updateDrivingSessionsInfos(uuidModifiedDrivingSessions, newDrivingSessionName):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    conn = MCADataBaseAccess_create_connection()
    with conn:
        sql = ''' UPDATE drivingsessions
                  SET name = ? 
                  WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, (newDrivingSessionName, uuidModifiedDrivingSessions))
        conn.commit()


def MCADataBaseAccess_fetchDrivingSessionsInfos(uuidDrivingSessionInfoWantedToBeFetch):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = MCADataBaseAccess_create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT * FROM drivingsessions WHERE id = ?"

        cur.execute(sql, (uuidDrivingSessionInfoWantedToBeFetch, ))
        rows = cur.fetchall()

        for row in rows:
            print(row)


def MCADataBaseAccess_fetchAllDrivingSessions():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = MCADataBaseAccess_create_connection()
    with conn:
        cur = conn.cursor()
        sql = "SELECT * FROM drivingsessions "

        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            print(row)  
         return rows






#
# Helper functions
#

def MCADataBaseAccess_create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    database = r"/Users/malo/Desktop/myConduiteAccompagnee/@sandboxes/2.serverWithDatabase/mcaDatabase.db"
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)

    return conn







if __name__ == "__main__":
    app.run(debug=True)


