import numpy as np


def hits_model(M, error_authority, error_hub):
    M_T = M.T

    authority_num = len(M[0])
    authority_score = np.ones(authority_num, dtype=float)
    authority_score_ = np.zeros(authority_num, dtype=float)
    iteration = 0
    while np.sum((authority_score - authority_score_) ** 2) ** 0.5 > error_authority:
        authority_score_ = authority_score
        authority_score = np.dot(np.dot(M_T, M), authority_score)  # In+1 =   M * M.T * In
        authority_score = authority_score / (sum(authority_score**2)**0.5) # 归一化
        iteration += 1
        print('authority正在进行第', iteration, '次迭代……')

    hub_num = len(M)
    hub_score = np.ones(hub_num, dtype=float)
    hub_score_ = np.zeros(hub_num, dtype=float)
    iteration = 0
    while np.sum((hub_score - hub_score_) ** 2) ** 0.5 > error_hub:
        hub_score_ = hub_score
        hub_score = np.dot(np.dot(M, M_T), hub_score)  # In+1 = M.T * M * In
        hub_score = hub_score / (sum(hub_score**2)**0.5)    # 归一化
        iteration += 1
        print('hub正在进行第', iteration, '次迭代……')

    return authority_score, hub_score