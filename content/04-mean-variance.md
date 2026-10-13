## 1. 여러 위험자산으로 넓히는 평균·분산 분석

두 위험자산에서는 첫 자산의 비중 $w$만 정하면 둘째 비중은 $1-w$였다. 자산이 $n$개면 비중은 $w_1,\ldots,w_n$이고 합계가 1이라는 조건 아래 $n-1$개를 독립적으로 고를 수 있다. 위험 계산에 필요한 공분산 항도 자산쌍마다 생긴다.

벡터는 비중과 예상 수익률을, 행렬은 모든 자산쌍의 공분산을 한데 적는다. 이 표기 덕분에 두 자산에서 배운 최적화 원리를 $n$개 자산에 그대로 적용할 수 있다.

## 2. 평균·분산 선택의 질문을 먼저 고정하기

평균·분산 분석은 가능한 모든 비중 가운데 **같은 기대수익률에서 분산이 가장 낮은 조합**을 찾는 문제다. 이렇게 얻은 점들의 집합이 최소분산 경계다. 그중 최소분산점보다 기대수익률이 높은 쪽을 효율적 프런티어라고 부른다. 위험에 비해 기대수익이 낮은 아래쪽 가지는 같은 위험에서 더 높은 평균을 주는 조합에 지배된다.

우선 기대수익률 벡터와 공분산행렬이 주어지고 공매도가 가능하다고 가정한다. 뒤에서 무위험자산을 추가하며, 거래 제약이나 추정 오차를 반영할 때는 허용 비중과 입력값을 다시 지정한다.

## 3. 네 단계로 읽는 계산 지도

앞으로 세 종류의 해가 나온다. 목표수익률 $m$에 대한 최소분산 해는 **평균을 고정한 채** 위험을 최소화한다. 글로벌 최소분산 포트폴리오(GMVP)는 **평균 목표 없이** 위험 자체를 최소화한다. 접점 포트폴리오는 무위험자산이 있을 때 **샤프비율**을 최대화한다.

세 문제는 목적함수와 제약이 다르므로 같은 비중을 줄 필요가 없다. 계산 순서는 비중·평균·공분산의 행렬 표현, 목표별 경계, GMVP, 무위험자산을 포함한 접점이다.

## 4. 벡터·전치·내적을 수익률에 연결하기

$n$개 자산의 기대수익률을 열벡터 $\boldsymbol\mu=(\mu_1,\ldots,\mu_n)^\top$, 비중을 $\mathbf w=(w_1,\ldots,w_n)^\top$로 쓴다. 전치 $\mathbf w^\top$는 $n\times1$ 열벡터를 $1\times n$ 행벡터로 바꾼다. 그러므로 행벡터와 열벡터의 곱은 하나의 숫자인 내적이 된다.

$$
\mu_p=\mathbf w^\top\boldsymbol\mu=\sum_{i=1}^n w_i\mu_i,\qquad
\mathbf 1^\top\mathbf w=\sum_{i=1}^n w_i=1.
$$

예를 들어 $\mathbf w=(.5,.3,.2)^\top$, $\boldsymbol\mu=(.08,.12,.16)^\top$이면 $\mu_p=.5(.08)+.3(.12)+.2(.16)=.108$이다. $\mathbf w^\top\boldsymbol\mu$는 $(1\times n)(n\times1)$의 곱이므로 숫자 하나다. 비중에 대한 gradient $\nabla_{\mathbf w}(\mathbf w^\top\boldsymbol\mu)=\boldsymbol\mu$는 다른 비중을 고정한 한계효과를 모은 벡터다.

다만 $\mathbf1^\top\mathbf w=1$을 유지하려면 한 비중을 늘릴 때 다른 비중을 줄여야 한다. $\mathbf e_i$를 $i$번째 성분만 1인 표준기저벡터라 하자. 자산 $j$에서 $i$로 $\varepsilon$만큼 옮기는 변화 $\Delta\mathbf w=\varepsilon(\mathbf e_i-\mathbf e_j)$는 합계가 0이고, 평균 변화는 정확히 $\Delta\mu_p=\varepsilon(\mu_i-\mu_j)$다. 개별 편미분 $\mu_i$와 **예산을 지키는 교체 거래의 효과**를 구분한다.

## 5. 공분산행렬과 이차형식의 뜻

공분산행렬 $\Omega$의 대각 원소는 각 자산의 분산 $\sigma_i^2$, 비대각 원소는 $\sigma_{ij}=\operatorname{Cov}(R_i,R_j)$이다. 공분산은 순서를 바꾸어도 같으므로 $\Omega$는 대칭행렬이다. 세 자산의 분산식은 다음과 같이 전개된다.

$$
\sigma_p^2=\mathbf w^\top\Omega\mathbf w
=\sum_{i=1}^3w_i^2\sigma_i^2
+2w_1w_2\sigma_{12}+2w_1w_3\sigma_{13}+2w_2w_3\sigma_{23}.
$$

공분산 항의 계수 2는 $(w_1X_1+w_2X_2+w_3X_3)^2$를 전개할 때 $X_iX_j$와 $X_jX_i$가 함께 나오기 때문이다. $\Omega\mathbf w$의 $i$번째 성분은 $\sum_jw_j\operatorname{Cov}(R_i,R_j)=\operatorname{Cov}(R_i,R_p)$다. 대칭행렬의 이차형식을 미분하면 $\nabla_{\mathbf w}(\mathbf w^\top\Omega\mathbf w)=(\Omega+\Omega^\top)\mathbf w=2\Omega\mathbf w$다. 따라서 $2\Omega\mathbf w$는 다른 비중을 고정한 한계위험이다. 라그랑지안에 $\tfrac12\mathbf w^\top\Omega\mathbf w$를 쓰면 미분 결과가 $\Omega\mathbf w$로 간결해진다.

행렬식의 출발점은 $\mathbf R=(R_1,\ldots,R_n)^\top$와 $\boldsymbol\mu=E[\mathbf R]$에 대한 $\Omega=E[(\mathbf R-\boldsymbol\mu)(\mathbf R-\boldsymbol\mu)^\top]$이다. 이를 대입하면 임의의 $\mathbf a$에 대해 $\mathbf a^\top\Omega\mathbf a=E[(\mathbf a^\top(\mathbf R-\boldsymbol\mu))^2]\ge0$다. 모든 $\mathbf a\ne0$에서 부등식이 엄격할 때 양의 **정부호**이며 역행렬이 존재한다. 이후의 닫힌 형태 해는 이 더 강한 조건을 사용한다.

## 6. 세 위험자산의 평균과 분산을 직접 계산하기

세 자산을 비중 $(.5,.3,.2)$로 담고 기대수익률이 $(.08,.12,.16)$이면 기대수익률은 앞에서 계산한 10.8%다. 표준편차가 각각 10%, 15%, 20%이고 공분산이 $\sigma_{12}=.003$, $\sigma_{13}=.002$, $\sigma_{23}=.009$라면 분산은 다음과 같다.

$$
\begin{aligned}
\sigma_p^2={}&(.5)^2(.10)^2+(.3)^2(.15)^2+(.2)^2(.20)^2\\
&+2(.5)(.3)(.003)+2(.5)(.2)(.002)+2(.3)(.2)(.009)\\
={}&.008505,\qquad \sigma_p\simeq9.22\%.
\end{aligned}
$$

세 자산 중 표준편차가 가장 낮은 자산도 10%인데 조합의 표준편차는 그보다 낮다. 개별 자산의 평균과 분산만으로는 이 결과를 예측할 수 없고 **서로 함께 움직이는 정도**를 알아야 한다. 비중의 합이 1인지, 공분산행렬이 대칭인지, 분산이 음수가 아닌지도 계산마다 검산한다.

## 7. 자산이 늘면 투자기회집합이 어떻게 달라지나

두 위험자산의 모든 조합은 비중 하나로 움직이는 곡선이다. 셋 이상이면 비중을 둘 이상 독립적으로 바꿀 수 있어 평균·표준편차 평면에 더 많은 조합이 생긴다. 그러나 그중 효율적인 **바깥쪽 경계**만 투자자의 평균·분산 선택에 남는다. 그림에서 개별 자산 A·B·C보다 더 높은 평균과 더 낮은 위험을 함께 주는 혼합 비중이 있을 수 있다.

여러 자산을 섞으면 개별 자산보다 유리한 조합이 생기는 경우가 많다. 개별 자산이 경계에 놓이는지는 기대수익률과 공분산 구조에 달려 있다. 공매도를 금지하면 허용 비중의 영역이 좁아져 개별 자산이 제한된 효율적 경계의 끝점이 될 수도 있다.

## 8. 무위험자산이 없을 때 목표수익률별 최소분산 해

목표 기대수익률을 $m$이라고 하자. 총비중 $\mathbf 1^\top\mathbf w=1$과 평균 $\boldsymbol\mu^\top\mathbf w=m$을 동시에 만족하면서 $\tfrac12\mathbf w^\top\Omega\mathbf w$를 최소화한다. 두 제약의 승수 $\lambda,\gamma$를 둔 라그랑지안은 다음과 같다.

$$
L=\tfrac12\mathbf w^\top\Omega\mathbf w
+\gamma(m-\boldsymbol\mu^\top\mathbf w)
+\lambda(1-\mathbf 1^\top\mathbf w).
$$

비중에 대한 일계조건은 $\Omega\mathbf w-\gamma\boldsymbol\mu-\lambda\mathbf1=0$이다. $\Omega$가 역행렬을 가지면 $\mathbf w=\Omega^{-1}(\gamma\boldsymbol\mu+\lambda\mathbf1)$을 얻는다. 이 비중은 반드시 **두 제약**을 만족해야 하므로 다시 평균식과 합계식에 대입한다. $A=\mathbf1^\top\Omega^{-1}\mathbf1$, $B=\boldsymbol\mu^\top\Omega^{-1}\mathbf1$, $C=\boldsymbol\mu^\top\Omega^{-1}\boldsymbol\mu$라 두면

$$
\begin{pmatrix}C&B\\B&A\end{pmatrix}
\begin{pmatrix}\gamma\\\lambda\end{pmatrix}
=\begin{pmatrix}m\\1\end{pmatrix}.
$$

첫째 식에 $A$, 둘째 식에 $B$를 곱해 빼면 $(AC-B^2)\gamma=Am-B$다. 둘째 식에 $C$, 첫째 식에 $B$를 곱해 빼면 $(AC-B^2)\lambda=C-Bm$이다. 따라서

$$
\Delta=AC-B^2,\qquad
\gamma=\frac{Am-B}{\Delta},\qquad
\lambda=\frac{C-Bm}{\Delta}
$$

를 얻는다. $A,B,C$는 긴 행렬 곱을 세 숫자로 요약한 표기다. 공분산행렬이 양의 정부호이고 자산들의 기대수익률이 모두 같지 않으면 $\Delta>0$이다. 이 조건은 목표 평균과 비중 합계가 독립적인 제약임을 보장한다.

이로써 $\mathbf w(m)=\Omega^{-1}(\gamma\boldsymbol\mu+\lambda\mathbf1)$의 모든 계수가 정해졌다. 일계조건의 해를 $\mathbf w_*$라 하고 같은 두 제약을 만족하는 다른 비중을 $\mathbf w_*+\mathbf u$라 쓰면 $\mathbf1^\top\mathbf u=\boldsymbol\mu^\top\mathbf u=0$이다. 따라서

$$
(\mathbf w_*+\mathbf u)^\top\Omega(\mathbf w_*+\mathbf u)
=\mathbf w_*^\top\Omega\mathbf w_*+\mathbf u^\top\Omega\mathbf u.
$$

교차항은 $\Omega\mathbf w_*=\gamma\boldsymbol\mu+\lambda\mathbf1$ 때문에 0이다. $\Omega$가 양의 정부호면 $\mathbf u\ne0$에 대해 마지막 항이 양수다. 그러므로 이 해는 공매도를 허용한 제약집합에서 **유일한 전역 최소해**다.

## 9. 평균·분산 경계의 방정식을 끝까지 유도하기

앞에서 구한 $\mathbf w$에 $\Omega$를 곱하면 $\Omega\mathbf w=\gamma\boldsymbol\mu+\lambda\mathbf1$이다. 왼쪽에 $\mathbf w^\top$를 곱하면 분산이 $\sigma_p^2=\gamma\mathbf w^\top\boldsymbol\mu+\lambda\mathbf w^\top\mathbf1=\gamma m+\lambda$가 된다. 승수 값을 대입해 정리하면

$$
\sigma_p^2(m)=\frac{Am^2-2Bm+C}{\Delta}
=\frac1A+\frac{A}{\Delta}\left(m-\frac BA\right)^2.
$$

전개를 거꾸로 확인하면 $Am^2-2Bm+C=A(m-B/A)^2+(AC-B^2)/A$다. 분모 $\Delta=AC-B^2$를 적용할 때 상수항이 $1/A$가 되는 과정을 생략하지 않는 이유다.

따라서 $\mu_G=B/A$, $\sigma_G^2=1/A$라 쓰면 분산을 가로축에 둔 그림에서는 $\sigma_p^2=\sigma_G^2+(A/\Delta)(m-\mu_G)^2$가 **옆으로 열린 포물선**이다. 표준편차를 가로축에 두면 같은 식을

$$
\frac{\sigma_p^2}{\sigma_G^2}
-\frac{(m-\mu_G)^2}{\Delta/A^2}=1
$$

로 써서 쌍곡선의 두 가지로 읽는다. $m=\mu_G+d$와 $m=\mu_G-d$는 위험이 같고, 평균이 높은 쪽이 다른 쪽을 지배한다. 따라서 효율적 프런티어는 $m\ge\mu_G$인 **위쪽 가지**다. $\Delta=0$이면 서로 다른 목표 평균으로 경계를 그리는 이 방식이 성립하지 않는다.

## 10. 글로벌 최소분산 포트폴리오를 찾기

앞의 완전제곱식은 $m=B/A$일 때 분산이 가장 작다고 곧바로 알려준다. 따라서 GMVP의 기대수익률과 분산은 $\mu_G=B/A$, $\sigma_G^2=1/A$다. 이 값을 승수식에 넣으면 $\gamma=0$, $\lambda=1/A$가 되어 비중도 얻는다.

$$
\mathbf w_G=\frac{\Omega^{-1}\mathbf1}{\mathbf1^\top\Omega^{-1}\mathbf1},
\qquad \mathbf1^\top\mathbf w_G=1.
$$

GMVP 비중은 주어진 공분산행렬만으로 결정된다. 기대수익률 벡터 $\boldsymbol\mu$는 이 포트폴리오의 평균 $B/A$를 평가하고 효율적 가지의 다른 점을 선택할 때 필요하다. 공매도 금지 제약이 있다면 음의 비중이 나온 경우 제약을 포함해 다시 최적화한다.

목표 평균을 거치지 않고도 같은 해를 증명할 수 있다. $\tfrac12\mathbf w^\top\Omega\mathbf w+\lambda(1-\mathbf1^\top\mathbf w)$를 미분하면 $\Omega\mathbf w=\lambda\mathbf1$이고, 합계 조건으로 $\lambda=1/A$다. 총비중만 1인 임의의 다른 비중을 $\mathbf w_G+\mathbf u$로 쓰면 $\mathbf1^\top\mathbf u=0$이고

$$
(\mathbf w_G+\mathbf u)^\top\Omega(\mathbf w_G+\mathbf u)
=\frac1A+\mathbf u^\top\Omega\mathbf u\ge\frac1A.
$$

교차항은 $\Omega\mathbf w_G=\mathbf1/A$와 $\mathbf1^\top\mathbf u=0$ 때문에 사라진다. 기대수익률을 쓰지 않고도 GMVP가 전역 최소라는 점이 드러난다.

## 11. 두 포트폴리오로 경계 전체를 만드는 이유

슬라이드 8의 승수를 모으면 $\mathbf w(m)=\mathbf w_G+(m-\mu_G)\mathbf h$로 쓸 수 있다. 여기서 $\mathbf h=\Omega^{-1}(A\boldsymbol\mu-B\mathbf1)/\Delta$이며 $\mathbf1^\top\mathbf h=0$, $\boldsymbol\mu^\top\mathbf h=1$이다. 따라서 목표 평균을 $d$만큼 높이면 비중은 $d\mathbf h$만큼 바뀐다. 서로 다른 목표수익률 $m_a,m_b$의 경계 포트폴리오를 알면 다른 $m$의 비중도 두 비중의 선형결합으로 표현된다.

$$
\mathbf w(m)=t\mathbf w(m_a)+(1-t)\mathbf w(m_b),
\qquad t=\frac{m_b-m}{m_b-m_a}.
$$

$t m_a+(1-t)m_b=m$이므로 이 결합은 합계 비중 1과 목표 평균 $m$을 동시에 만족한다. 더구나 $\mathbf w(m)$ 자체가 $m$의 일차함수이므로 결합한 비중이 바로 목표별 최소분산 해다. 서로 다른 두 **경계 포트폴리오**로 경계의 다른 점을 만들 수 있다는 성질이 **two-fund separation**이다. $m$이 두 기준 평균 밖이면 계수 하나가 음수가 되어 해당 기준 포트폴리오의 공매도가 필요하다.

## 12. 무위험자산을 넣으면 생기는 접선

두 자산 장에서 위험자산 조합 $P$와 무위험자산을 섞으면 $\mu_c=r_f+y(\mu_P-r_f)$, $\sigma_c=y\sigma_P$라는 직선을 얻었다. 여러 자산에서도 내부 조합 $P$를 바꿀 때 이 직선의 기울기 $S_P=(\mu_P-r_f)/\sigma_P$를 비교한다.

위험자산의 경계를 분산 함수 $v(m)=(Am^2-2Bm+C)/\Delta$로 나타내면 $S(m)=(m-r_f)/\sqrt{v(m)}$다. 내부 접점에서 $S'(m)=0$을 정리하면 $2v(m)=(m-r_f)v'(m)$이고, $v'(m)=2(Am-B)/\Delta$를 넣으면

$$
m_T=\frac{C-Br_f}{B-Ar_f}\qquad(B-Ar_f>0)
$$

를 얻는다. $m_T-\mu_G=\Delta/[A(B-Ar_f)]>0$이므로 접점은 최소분산점보다 평균이 높은 **효율적 가지**에 있다. 이 식은 접점의 평균 수익률을 주며, 비중 벡터는 다음 슬라이드에서 구한다. 도함수 조건은 위험자산 경계의 접선 기울기가 무위험점에서 그은 직선의 기울기와 같다는 기하학적 조건이다.

## 13. 접점을 찾는 첫 단계: 초과수익의 위험 최소화

각 위험자산의 초과 기대수익률을 $\mathbf e=\boldsymbol\mu-r_f\mathbf1$이라 하자. 위험자산에 넣는 전체 비중 $\mathbf w_c$가 목표 초과수익률 $e_c=\mathbf e^\top\mathbf w_c$를 만들 때 분산이 최소인 비중을 찾는다. 이 단계에서는 **위험자산 비중의 합을 1로 고정하지 않는다**. 나머지 금액이 무위험자산에 들어가기 때문이다.

$$
L=\tfrac12\mathbf w_c^\top\Omega\mathbf w_c
+\theta(e_c-\mathbf e^\top\mathbf w_c),
\qquad \nabla_{\mathbf w_c}L=\Omega\mathbf w_c-\theta\mathbf e=\mathbf0.
$$

따라서 $\mathbf w_c=\theta\Omega^{-1}\mathbf e$다. 제약식 $\mathbf e^\top\mathbf w_c=e_c$에 대입하면 $\theta=e_c/(\mathbf e^\top\Omega^{-1}\mathbf e)$를 얻는다. 분모는 $\Omega$가 양의 정부호이고 $\mathbf e\ne\mathbf0$일 때 양수다. 목표 초과수익 $e_c$는 전체 크기만 바꾸고 위험자산 **서로 간의 비율**은 $\Omega^{-1}\mathbf e$가 정한다.

해를 다시 이차형식에 넣으면 $\sigma_c^2=\theta^2\mathbf e^\top\Omega^{-1}\mathbf e=e_c^2/(\mathbf e^\top\Omega^{-1}\mathbf e)$다. $e_c>0$이면 $e_c/\sigma_c=\sqrt{\mathbf e^\top\Omega^{-1}\mathbf e}$가 목표 초과수익의 크기와 무관하다. 목적함수가 엄격히 볼록하므로 이 일계조건의 해가 해당 목표의 유일한 최소분산 해다.

## 14. 둘째 단계: 위험자산 내부 비중을 1로 정규화하기

접점 포트폴리오 $P$는 위험자산만으로 이루어진 **내부 조합**이므로 $\mathbf1^\top\mathbf w_P=1$이어야 한다. 앞의 방향 벡터 $\Omega^{-1}\mathbf e$를 합계가 1이 되도록 나누면

$$
\mathbf w_P=\frac{\Omega^{-1}(\boldsymbol\mu-r_f\mathbf1)}
{\mathbf1^\top\Omega^{-1}(\boldsymbol\mu-r_f\mathbf1)}
=\frac{\Omega^{-1}(\boldsymbol\mu-r_f\mathbf1)}{B-Ar_f}.
$$

$B-Ar_f>0$이면 이 정규화의 초과 기대수익이 양수이며 샤프비율은 $\sqrt{\mathbf e^\top\Omega^{-1}\mathbf e}$다. $B-Ar_f=0$이면 방향벡터의 비중 합이 0이어서 유한한 합계 1 포트폴리오로 정규화할 수 없다. 전체 계좌에서는 위험자산에 $y\mathbf w_P$, 무위험자산에 $1-y$를 배분한다.

$B-Ar_f<0$이면 분모로 나누는 순간 $\Omega^{-1}\mathbf e$의 방향이 뒤집힌다. 그 결과 위 식은 합계 1인 위험자산 조합이지만 **양의 초과수익을 주는 최대 샤프비율 접점**은 아니다. 따라서 접점 공식은 역행렬과 분모의 존재만 확인해서 끝내지 않고, $\mathbf e\ne0$, 분모의 부호, 허용된 공매도·차입 범위를 함께 확인해야 한다.

## 15. 두 위험자산 공식과 같은 답인지 검산하기

두 자산이면 $\mathbf e=(e_1,e_2)^\top$이고 $\Omega=\begin{pmatrix}\sigma_1^2&\sigma_{12}\\\sigma_{12}&\sigma_2^2\end{pmatrix}$이다. 역행렬에 $\mathbf e$를 곱한 뒤 두 성분의 합으로 나누면 첫 자산의 접점 비중은

$$
w_{P,1}=\frac{\sigma_2^2e_1-\sigma_{12}e_2}
{(\sigma_2^2-\sigma_{12})e_1+(\sigma_1^2-\sigma_{12})e_2},
\qquad w_{P,2}=1-w_{P,1}.
$$

예를 들어 $\mu=(.10,.14)$, $r_f=.05$, $\sigma_1=.15$, $\sigma_2=.20$, $\rho=.20$이면 $\sigma_{12}=.006$이고 $e_1=.05,e_2=.09$다. 분자는 $.04(.05)-.006(.09)=.00146$, 분모는 $.034(.05)+.0165(.09)=.003185$이므로 $w_{P,1}\simeq45.84\%$, $w_{P,2}\simeq54.16\%$다. 두 자산에서 직접 미분해 얻은 비중과 일치한다. 역행렬 식의 공통 분모 $\sigma_1^2\sigma_2^2-\sigma_{12}^2$는 정규화 과정에서 약분된다.

## 16. 두 프런티어를 한 그림에서 비교하기

무위험자산이 없을 때 선택 가능한 최상단은 평균·분산 경계의 위쪽 가지다. 양의 초과수익을 주는 접점 $P$가 존재하면, 무위험자산을 허용한 뒤에는 $r_f$에서 $P$를 지나는 직선이 효율적 선택선이 된다.

$$
\mu_c=r_f+\frac{\mu_P-r_f}{\sigma_P}\,\sigma_c
\quad(y\ge0),\qquad
\frac{\mu_c-r_f}{\sigma_c}=\frac{\mu_P-r_f}{\sigma_P}.
$$

이를 부등식으로도 확인할 수 있다. 슬라이드 13에서 $S_T=\sqrt{\mathbf e^\top\Omega^{-1}\mathbf e}$였으므로 임의의 위험자산 조합 $Q$에는 $\mu_Q-r_f\le S_T\sigma_Q$가 성립한다. $Q$에 전체 자금의 $y\ge0$을 배분하면 같은 위험 $\sigma_c=y\sigma_Q$에서

$$
\mu_c=r_f+y(\mu_Q-r_f)\le r_f+S_T\sigma_c.
$$

접점 조합에서는 등호가 성립한다. 이 부등식이 접점 직선보다 위에 실현 가능한 점이 없다는 수학적 이유다. $y>1$ 구간은 같은 $r_f$로 차입할 수 있을 때 직선으로 이어진다.

## 17. 평균·분산 선택에서 CAPM으로 넘어가기

지금까지는 기대수익률 $\boldsymbol\mu$와 공분산 $\Omega$가 주어졌을 때 투자자 한 명의 최적 비중을 구했다. CAPM은 투자자들이 공통 기대를 가지고, 위험자산의 총수요가 실제 공급과 같다는 **시장청산** 조건을 더한다. 이때 접점 포트폴리오를 시장포트폴리오에 연결하면 개별 자산의 **시장과 함께 움직이는 위험**이 기대수익률에 어떻게 반영되는지 설명할 수 있다.

공통의 접점 비중이 시장 비중 $\mathbf w_M$와 같다면 $\Omega\mathbf w_M=k(\boldsymbol\mu-r_f\mathbf1)$인 양의 상수 $k$가 존재한다. 양변을 정리하고 시장 비중으로 가중해 $k$를 제거하면 $\mu_i-r_f=[\operatorname{Cov}(R_i,R_M)/\operatorname{Var}(R_M)](\mu_M-r_f)$다. 이 괄호가 $\beta_i$다. CAPM의 가격식은 개인의 최적화에 **공통 기대·무위험 차입과 대출·시장청산**을 추가한 결과다. 역사적 회귀로 구한 베타는 이 식을 실증적으로 적용할 때 필요한 위험 추정치다.
