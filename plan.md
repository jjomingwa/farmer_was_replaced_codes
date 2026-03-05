# 구현 상세 계획서: 드론 동기화 및 효율성 개선

## 1. 접근 방식 및 아키텍처
리서치 결과 발견된 드론 방황 및 자원 고갈 문제를 해결하기 위해 **동기화(Synchronization)**와 **비용 최적화(Cost Optimization)**를 적용합니다.

- **동기화 레이어**: `for_all` 함수가 모든 드론의 종료를 보장하도록 수정하여, 확실히 필드가 비워진 후 다음 단계(파종)가 진행되게 합니다.
- **최적화 워커 로직**: 이미 다른 체인에 의해 식물이 심어진 타일은 방문하지 않도록 조건문을 강화하여 드론의 불필요한 이동을 최소화합니다.
- **자원 관리**: 드론 한도(32개)를 효율적으로 사용하기 위해 메인 드론과 보조 드론의 역할을 명확히 구분합니다.

- [x] `functions.py`: `for_all` 함수에 `wait_for` 로직 추가 (완료)
- [x] `Mega_Crops.py`: `mixed_worker_logic`의 중복 방문 방지 로직 추가 (완료)
- [x] `Mega_Crops.py`: `mega_mixed_cultivation`의 단계 간 동기화 보강 (완료)

## 2. 수정 대상 파일 및 경로
- `functions.py`: 공통 병렬 유틸리티 수정
- `Mega_Crops.py`: 혼합 재배 워커 및 메인 함수 수정

## 3. 코드 스니펫 (Code Snippets)

### 3.1 동기화가 보장된 for_all (`functions.py`)
```python
def for_all(f):
    drones = []
    def row_task():
        for _ in range(WORLD_SIZE - 1):
            f()
            move(East)
        f()
    
    for _ in range(WORLD_SIZE):
        d = spawn_drone(row_task)
        if d == None:
            row_task() # 드론 한도 도달 시 직접 수행
        else:
            drones.append(d)
        move(North)
    
    # 생성된 모든 드론이 작업을 마칠 때까지 대기
    for d in drones:
        wait_for(d)
    
    # 작업 완료 후 원점 복귀 (동기화 보장)
    go_zero()
```

### 3.2 효율성이 개선된 워커 로직 (`Mega_Crops.py`)
```python
def mixed_worker_logic(start_x):
    for start_y in range(WORLD_SIZE):
        go(start_x, start_y)
        
        # 1단계: 현재 타일이 비어있을 때만 새로운 체인 시작
        if get_entity_type() == None:
            plant(Entities.Bush)
            
            # 2단계: 체인 추적
            for i in range(5):
                companion = get_companion()
                if companion == None: break
                
                target_type = companion[0]
                pos = companion[1]
                tx = pos[0]
                ty = pos[1]
                
                go(tx, ty)
                
                # 타겟 위치가 비어있을 때만 심기, 아니면 체인 중단 (중복 방지)
                if get_entity_type() == None:
                    if target_type == Entities.Carrot: till()
                    plant(target_type)
                else:
                    break # 이미 식물이 심어져 있다면 효율을 위해 중단
```

## 4. 고려 사항 및 트레이드오프
- **동기화 대기 시간**: `wait_for`를 사용하면 필드 전체가 비워지는 것을 기다려야 하므로 시작 시 약간의 지연이 발생하지만, 파종 단계에서 드론 자원을 100% 활용할 수 있게 되어 전체 속도는 향상됩니다.
- **체인 중단 전략**: `break`를 통해 이미 심어진 타일을 만나면 체인을 끊음으로써 이동 거리를 단축하지만, 완벽한 동반 식물 배치를 위해서는 약간의 보강이 필요할 수 있습니다. 현재는 "방황 방지"와 "속도"에 우선순위를 둡니다.
- **메모리 사용**: `drones` 리스트에 핸들을 저장하므로, 32개 드론의 핸들을 관리하는 메모리가 추가로 소모되나 이는 매우 미미한 수준입니다.
